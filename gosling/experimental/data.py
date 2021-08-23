import abc
from dataclasses import dataclass, field
import functools
import itertools
import hashlib
import mimetypes
import pathlib
import threading
import time
import uuid
import weakref
from typing import (
    IO,
    Any,
    Awaitable,
    Callable,
    Generator,
    Iterable,
    MutableMapping,
    Optional,
    Union,
)

import portpicker
import starlette.applications
import starlette.endpoints
import starlette.requests
import starlette.responses
import starlette.middleware.cors
import starlette.routing
import uvicorn

import gosling.data as url_loaders


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

    def start(
        self,
        port: Optional[int] = None,
        timeout: int = 1,
        daemon: bool = True,
        log_level: str = "warning",
    ):

        if self._server_thread is not None:
            return self

        config = uvicorn.Config(
            app=self.app,
            port=port or portpicker.pick_unused_port(),
            timeout_keep_alive=timeout,
            log_level=log_level,
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
    file: IO[bytes], start: int = 0, end: int = None, block_size: int = 65535
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

        media_type, _ = mimetypes.guess_type(self.filepath)
        media_type = media_type or "application/octet-stream"
        content_range = request.headers.get("range")

        file = self.filepath.open("rb")
        file_size = self.filepath.stat().st_size

        headers = self.headers.copy()

        if content_range is not None:
            range_start, range_end = parse_content_range(content_range, file_size)
            content_length = (range_end - range_start) + 1
            file = ranged(file, start=range_start, end=range_end + 1)
            headers["Content-Range"] = f"bytes {range_start}-{range_end}/{file_size}"

            return starlette.responses.StreamingResponse(
                content=file,
                media_type=media_type,
                status_code=206,
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(content_length),
                    **headers,
                },
            )

        return starlette.responses.FileResponse(
            self.filepath, headers=headers, media_type=media_type
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


@dataclass(frozen=True)
class Tileset:
    tiles: Callable[[Iterable[str]], list]
    info: Callable[[], dict[str, Any]]
    guid: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass(frozen=True)
class TilesetResource:
    tileset: Tileset
    provider: "Provider"

    @property
    def guid(self) -> str:
        return self.tileset.guid

    @property
    def url(self) -> str:
        return f"{self.provider.url}/api/v1/tileset_info/?d={self.tileset.guid}"


def create_resources_route(
    resources: MutableMapping[str, Resource]
) -> starlette.routing.Route:
    def endpoint(request: starlette.requests.Request):
        resource = resources.get(request.path_params["guid"])
        if not resource:
            return starlette.responses.Response(None, 404)
        return resource.get(request)

    return starlette.routing.Route("/{guid:path}", endpoint=endpoint)


def get_list(query: str, field: str) -> list[str]:
    """Parse chained query params into list.
    >>> get_list("d=id1&d=id2&d=id3", "d")
    ["id1", "id2", "id3"]
    >>> get_list("d=1&e=2&d=3", "d")
    ["1", "3"]
    """
    kv_tuples = [x.split("=") for x in query.split("&")]
    return [v for k, v in kv_tuples if k == field]


# adapted from https://github.com/higlass/higlass-python/blob/b3be6e49cbcab6be72eb0ad65c68a286161b8682/higlass/server.py#L169-L199
def create_tileset_route(tileset_resources: MutableMapping[str, TilesetResource]):
    def tileset_info(request: starlette.requests.Request):
        guids = get_list(request.url.query, "d")
        info = {
            guid: tileset_resources[guid].tileset.info()
            if guid in tileset_resources
            else {"error": f"No such tileset with guid: {guid}"}
            for guid in guids
        }
        return starlette.responses.JSONResponse(info)

    def tiles(request: starlette.requests.Request):
        requested_tids = set(get_list(request.url.query, "d"))
        if not requested_tids:
            return starlette.responses.JSONResponse(
                {"error": "No tiles requested"}, 400
            )

        tiles: list = []
        for guid, tids in itertools.groupby(
            iterable=sorted(requested_tids), key=lambda tid: tid.split(".")[0]
        ):
            tileset_resource = tileset_resources.get(guid)
            if not tileset_resource:
                return starlette.responses.JSONResponse(
                    {"error": f"No tileset found for requested guid: {guid}"}, 400
                )
            tiles.extend(tileset_resource.tileset.tiles(list(tids)))
        data = {tid: tval for tid, tval in tiles}
        return starlette.responses.JSONResponse(data)

    return starlette.routing.Mount(
        "/api/v1",
        routes=[
            starlette.routing.Route("/tileset_info", endpoint=tileset_info),
            starlette.routing.Route("/tiles", endpoint=tiles),
        ],
    )


class Provider(BackgroundServer):
    def __init__(self, allowed_origins: Optional[list[str]] = None):
        self._resources: weakref.WeakValueDictionary[
            str, Resource
        ] = weakref.WeakValueDictionary()
        self._tilesets: weakref.WeakValueDictionary[
            str, TilesetResource
        ] = weakref.WeakValueDictionary()

        routes = [
            create_tileset_route(self._tilesets),
            create_resources_route(self._resources),
        ]

        app = starlette.applications.Starlette(routes=routes)

        if allowed_origins:
            # configure cors
            app.add_middleware(
                starlette.middleware.cors.CORSMiddleware,
                allow_origins=allowed_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        super().__init__(app)

    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"

    def create(
        self,
        content: str = "",
        filepath: str = "",
        handler: Optional[CustomHandler] = None,
        tileset: Optional[Tileset] = None,
        headers: Optional[dict[str, str]] = None,
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ) -> Union[Resource, TilesetResource]:

        sources = sum(map(bool, (content, filepath, handler, tileset)))
        if sources != 1:
            raise ValueError(
                "Must provide exactly one of content, filepath, handler, tileset"
            )

        headers = headers or {}
        resource: Union[Resource, TilesetResource]

        if tileset:
            resource = TilesetResource(tileset, provider=self)
            self._tilesets[resource.guid] = resource
        else:
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


def _hash_filepath(path: str):
    return _compute_data_hash(str(pathlib.Path(path)))


class GoslingDataServer:
    """Backend server for Gosling datasets."""

    def __init__(self) -> None:
        self._provider: Optional[Provider] = None
        # We need to keep references to served resources, because the background
        # server uses weakrefs.
        self._resources: dict[str, Union[Resource, TilesetResource]] = {}

    def reset(self) -> None:
        if self._provider is not None:
            self._provider.stop()
        self._resources = {}

    def __call__(self, data: Union[str, Tileset], port: Optional[int] = None):
        if self._provider is None:
            self._provider = Provider(allowed_origins=["*"]).start(port=port)

        if port is not None and port != self._provider.port:
            self._provider.stop().start(port=port)

        if isinstance(data, Tileset):
            resource_id = data.guid
            if data.guid not in self._resources:
                self._resources[resource_id] = self._provider.create(tileset=data)
        else:
            resource_id = _hash_filepath(data)
            if resource_id not in self._resources:
                self._resources[resource_id] = self._provider.create(filepath=data)

        return self._resources[resource_id].url


def with_default(url_loader):
    """Delegates data creation method based on whether path is url or local file."""

    def decorator(file_loader):
        def wrapper(*args, **kwargs):
            if "url" in kwargs and "filepath" in kwargs:
                raise ValueError("Must provide one of url or filepath")

            if "url" in kwargs:
                return url_loader(*args, **kwargs)

            if "filepath" in kwargs:
                return file_loader(*args, **kwargs)

            if len(args) != 1:
                raise ValueError(
                    "Can only provide url or filepath as positional argument."
                )

            loader = url_loader if args[0] in ["http://", "http://"] else file_loader
            return loader(*args, **kwargs)

        return wrapper

    return decorator


data_server = GoslingDataServer()


@with_default(url_loaders.csv)
def csv(filepath: str, **kwargs):
    url = data_server(filepath, port=kwargs.pop("port", None))
    return dict(type="csv", url=url, **kwargs)


@with_default(url_loaders.json)
def json(filepath: str, **kwargs):
    url = data_server(filepath, port=kwargs.pop("port", None))
    return dict(type="json", url=url, **kwargs)


@with_default(url_loaders.bigwig)
def bigwig(filepath: str, **kwargs):
    url = data_server(filepath, port=kwargs.pop("port", None))
    return dict(type="bigwig", url=url, **kwargs)


@with_default(url_loaders.beddb)
def beddb(filepath: str, **kwargs):
    try:
        from clodius.tiles.beddb import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "beddb" data-server.'
        )

    tileset = Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        guid=_hash_filepath(filepath),
    )
    url = data_server(tileset, port=kwargs.pop("port", None))
    return dict(type="beddb", url=url, **kwargs)


@with_default(url_loaders.vector)
def vector(filepath: str, **kwargs):
    try:
        from clodius.tiles.bigwig import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "vector" data-server.'
        )

    tileset = Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        guid=_hash_filepath(filepath),
    )
    url = data_server(tileset, port=kwargs.pop("port", None))
    return dict(type="vector", url=url, **kwargs)


@with_default(url_loaders.multivec)
def multivec(filepath: str, **kwargs):
    try:
        from clodius.tiles.multivec import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "multivec" data-server.'
        )

    tileset = Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        guid=_hash_filepath(filepath),
    )
    url = data_server(tileset, port=kwargs.pop("port", None))
    return dict(type="multivec", url=url, **kwargs)


@with_default(url_loaders.bam)
def bam(filepath: str, index_filename=None, chromsizes=None, **kwargs):
    try:
        from clodius.tiles.bam import tiles, tileset_info
    except ImportError:
        raise ImportError('You must have `clodius` installed to use "bam" data-server.')

    if not index_filename:
        index_filename = f"{filepath}.bai"

    tileset = Tileset(
        tiles=functools.partial(
            tiles, filepath, index_filename=index_filename, chromsizes=chromsizes
        ),
        info=functools.partial(tileset_info, filepath, chromsizes=chromsizes),
        guid=_hash_filepath(filepath),
    )
    url = data_server(tileset, port=kwargs.pop("port", None))
    return dict(type="bam", url=url, **kwargs)


@with_default(url_loaders.matrix)
def matrix(filepath: str, **kwargs):
    try:
        from clodius.tiles.cooler import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "matrix" data-server.'
        )

    tileset = Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info),
        guid=_hash_filepath(filepath),
    )
    url = data_server(tileset, port=kwargs.pop("port", None))
    return dict(type="matrix", url=url, **kwargs)
