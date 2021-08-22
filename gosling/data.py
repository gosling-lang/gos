import abc
import hashlib
import mimetypes
import pathlib
import threading
import time
import uuid
import weakref
from typing import IO, Awaitable, Callable, Generator, MutableMapping, Optional

import portpicker
import starlette.applications
import starlette.endpoints
import starlette.requests
import starlette.responses
import starlette.routing
import uvicorn

from gosling.schema import core


class BackgroundServer:
    _app: starlette.applications.Starlette
    _port: Optional[int]
    _server_thread: Optional[threading.Thread]
    _server: Optional[uvicorn.Server]

    def __init__(self, app: starlette.applications.Starlette):
        self._app = app
        self._port = None
        self._server_thread = None
        self._server = None

    @property
    def app(self) -> starlette.applications.Starlette:
        return self._app

    @property
    def port(self) -> int:
        if self._server_thread is None or self._port is None:
            raise RuntimeError("Server not running.")
        return self._port

    def stop(self):
        if self._server_thread is None:
            return self
        assert self._server is not None

        try:
            # queue exit event and wait for thread to terminate
            self._server.should_exit = True
            self._server_thread.join()
        finally:
            self._server = None
            self._server_thread = None

        return self

    def start(self, port: Optional[int] = None, timeout: int = 1, daemon: bool = True):

        if self._server_thread is not None:
            return self

        config = uvicorn.Config(
            app=self.app,
            port=port or portpicker.pick_unused_port(),
            timeout_keep_alive=timeout,
        )

        self._port = config.port
        self._server = uvicorn.Server(config=config)
        self._server_thread = threading.Thread(target=self._server.run, daemon=daemon)
        self._server_thread.start()

        # wait for the server to start
        while not self._server.started:
            time.sleep(1e-3)

        return self

    def __rich_repr__(self):
        for key in ("app", "port"):
            yield key, getattr(self, "_" + key)

    def __repr__(self):
        props = ", ".join(f"{k}={repr(v)}" for k, v in self.__rich_repr__())
        return f"{self.__class__.__name__}({props})"


def _compute_data_hash(data_str: str):
    return hashlib.md5(data_str.encode()).hexdigest()


class Resource(metaclass=abc.ABCMeta):
    def __init__(
        self,
        provider: "Provider",
        headers: dict[str, str],
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ):
        if route is not None and extension is not None:
            raise ValueError("Should only provide one of route or extension.")
        self.headers = headers
        if route is None:
            route = str(uuid.uuid4())
            if extension:
                route += "." + extension
        self._guid = route.lstrip("/")
        self._provider = provider

    @abc.abstractmethod
    def get(
        self, request: starlette.requests.Request
    ) -> Awaitable[starlette.responses.Response]:
        ...

    @property
    def guid(self) -> str:
        return self._guid

    @property
    def url(self) -> str:
        return f"{self._provider.url}/{self._guid}"

    def __rich_repr__(self):
        for key in ("guid", "url", "headers"):
            yield key, getattr(self, key)

    def __repr__(self):
        props = ", ".join(f"{k}={repr(v)}" for k, v in self.__rich_repr__())
        return f"{self.__class__.__name__}({props})"


class ContentResource(Resource):
    """Content Resource"""

    def __init__(
        self,
        content: str,
        provider: "Provider",
        headers: dict[str, str],
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ):
        self.content = content
        if route is None:
            route = _compute_data_hash(self.content)
            if extension is not None:
                route += "." + extension
                extension = None
        super().__init__(
            provider=provider, headers=headers, extension=extension, route=route
        )

    def get(self, _) -> starlette.responses.Response:
        return starlette.responses.Response(content=self.content, headers=self.headers)


# adapted from https://gist.github.com/tombulled/712fd8e19ed0618c5f9f7d5f5f543782
def ranged(
    file: IO[bytes], start: int = 0, end: int = None, block_size: int = 8192
) -> Generator[bytes, None, None]:
    """Read content range as generator from file object."""
    consumed = 0
    file.seek(start)

    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, "close"):
        file.close()


def parse_content_range(content_range: str, file_size: int) -> tuple[int, int]:
    """Parse 'Range' header into integer interval."""
    content_range = content_range.strip().lower()
    content_ranges = content_range.split("=")[-1]
    range_start, range_end, *_ = map(str.strip, (content_ranges + "-").split("-"))
    return (
        max(0, int(range_start)) if range_start else 0,
        min(file_size - 1, int(range_end)) if range_end else file_size - 1,
    )


# Supports range requests for reading bigwig files
# TODO: Explore using fsspec to support more than just local filesytem
class FileResource(Resource):
    """File Resource"""

    def __init__(
        self,
        filepath: str,
        provider: "Provider",
        headers: dict[str, str],
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ):
        self.filepath = pathlib.Path(filepath)
        super().__init__(
            provider=provider, headers=headers, extension=extension, route=route
        )

    def get(self, request: starlette.requests.Request) -> starlette.responses.Response:

        content_range = request.headers.get("range")

        file = self.filepath.open("rb")
        file_size = self.filepath.stat().st_size

        status_code = 200
        content_length = file_size
        headers = self.headers.copy()

        if content_range is not None:
            range_start, range_end = parse_content_range(content_range, file_size)
            content_length = (range_end - range_start) + 1
            file = ranged(file, start=range_start, end=range_end + 1)
            status_code = 206
            headers["Content-Range"] = f"bytes {range_start}-{range_end}/{file_size}"

        media_type, _ = mimetypes.guess_type(self.filepath)
        return starlette.responses.StreamingResponse(
            content=file,
            media_type=media_type or "application/octet-stream",
            status_code=status_code,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
                **headers,
            },
        )


CustomHandler = Callable[
    [starlette.requests.Request], Awaitable[starlette.responses.RedirectResponse]
]


class HandlerResource(Resource):
    def __init__(
        self,
        func: CustomHandler,
        provider: "Provider",
        headers: dict[str, str],
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ):
        self.func = func
        super().__init__(
            provider=provider, headers=headers, extension=extension, route=route
        )

    async def get(self, request: starlette.requests.Request):
        resp = await self.func(request)
        resp.headers.update(self.headers)
        return resp


def create_resources_route(
    resources: MutableMapping[str, Resource]
) -> starlette.routing.Route:
    def endpoint(request: starlette.requests.Request):
        path = request.url.path
        resource = resources.get(path.lstrip("/"))
        if not resource:
            return starlette.responses.Response(None, 404)
        return resource.get(request)

    return starlette.routing.Route("/*", endpoint=endpoint)


class Provider(BackgroundServer):

    _resources: MutableMapping[str, Resource]

    def __init__(self):
        self._resources = weakref.WeakValueDictionary()
        route = create_resources_route(self._resources)
        app = starlette.applications.Starlette(routes=[route])
        super().__init__(app)

    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"

    def create(
        self,
        content: str = "",
        filepath: str = "",
        handler: Optional[CustomHandler] = None,
        headers: Optional[dict[str, str]] = None,
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ) -> Resource:

        sources = sum(map(bool, (content, filepath, handler)))
        if sources != 1:
            raise ValueError(
                "Must provide exactly one of content, filepath, or handler"
            )

        headers = headers or {}
        resource: Resource

        if content:
            resource = ContentResource(
                content,
                headers=headers,
                extension=extension,
                provider=self,
                route=route,
            )
        elif filepath:
            resource = FileResource(
                filepath,
                headers=headers,
                extension=extension,
                provider=self,
                route=route,
            )
        elif handler:
            resource = HandlerResource(
                handler,
                headers=headers,
                extension=extension,
                provider=self,
                route=route,
            )
        else:
            raise ValueError("Must provide one of content, filepath, or handler.")

        self._resources[resource.guid] = resource
        self.start()
        return resource


class GoslingDataServer:
    """Backend server for Gosling datasets."""

    def __init__(self) -> None:
        self._provider: Optional[Provider] = None
        # We need to keep references to served resources, because the background
        # server uses weakrefs.
        self._resources: dict[str, Resource] = {}

    def reset(self) -> None:
        if self._provider is not None:
            self._provider.stop()
        self._resources = {}

    def __call__(self, filepath: str, port: Optional[int] = None):
        if self._provider is None:
            self._provider = Provider().start(port=port)

        if port is not None and port != self._provider.port:
            self._provider.stop().start(port=port)

        resource_id = _compute_data_hash(str(pathlib.Path(filepath)))
        if resource_id not in self._resources:
            self._resources[resource_id] = self._provider.create(
                filepath=filepath,
                headers={"Access-Control-Allow-Origin": "*"},
            )

        return self._resources[resource_id].url


data_server = GoslingDataServer()


def csv(filepath: str, **kwargs):
    url = data_server(filepath=filepath, port=kwargs.pop("port"))
    return core.DataDeep(type="csv", url=url, **kwargs)


def bigwig(filepath: str, **kwargs):
    url = data_server(filepath=filepath, port=kwargs.pop("port"))
    return core.DataDeep(type="bigwig", url=url, **kwargs)


def json(filepath: str, **kwargs):
    url = data_server(filepath=filepath, port=kwargs.pop("port"))
    return core.DataDeep(type="json", url=url, **kwargs)
