import abc
import itertools
import mimetypes
import pathlib
import uuid
import weakref
from dataclasses import dataclass, field
from typing import (
    IO,
    Awaitable,
    Dict,
    Generator,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Union,
)

import starlette.applications
import starlette.middleware.cors
import starlette.requests
import starlette.responses
import starlette.routing

from gosling.utils.core import _compute_data_hash

from ._background_server import BackgroundServer
from ._tilesets import Tileset


class Resource(metaclass=abc.ABCMeta):
    def __init__(
        self,
        provider: "Provider",
        headers: Dict[str, str],
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
        yield "url", self.url


class ContentResource(Resource):
    """Content Resource"""

    def __init__(
        self,
        content: str,
        provider: "Provider",
        headers: Dict[str, str],
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


def parse_content_range(content_range: str, file_size: int) -> Tuple[int, int]:
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
        filepath: pathlib.Path,
        provider: "Provider",
        headers: Dict[str, str],
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ):
        self.filepath = filepath
        extension = extension or filepath.suffix.lstrip(".")
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

    def __rich_repr__(self):
        yield "filepath", str(self.filepath)
        for tup in super().__rich_repr__():
            yield tup


@dataclass(frozen=True)
class TilesetResource:
    tileset: Tileset
    provider: "Provider"
    guid: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def url(self) -> str:
        return f"{self.provider.url}/api/v1/tileset_info/?d={self.guid}"

    def __rich_repr__(self):
        yield "url", self.url
        yield "type", self.tileset.type


def get_list(query: str, field: str) -> List[str]:
    """Parse chained query params into list.
    >>> get_list("d=id1&d=id2&d=id3", "d")
    ['id1', 'id2', 'id3']
    >>> get_list("d=1&e=2&d=3", "d")
    ['1', '3']
    """
    kv_tuples = [x.split("=") for x in query.split("&")]
    return [v for k, v in kv_tuples if k == field]


def create_resources_route(resources: MutableMapping[str, Resource]):
    def endpoint(request: starlette.requests.Request):
        resource = resources.get(request.path_params["guid"])
        if not resource:
            return starlette.responses.Response(None, 404)
        return resource.get(request)

    return starlette.routing.Route("/{guid:path}", endpoint=endpoint)


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
    _resources: MutableMapping[str, Resource]
    _tilesets: MutableMapping[str, TilesetResource]

    def __init__(self, allowed_origins: Optional[List[str]] = None):
        self._resources = weakref.WeakValueDictionary()
        self._tilesets = weakref.WeakValueDictionary()

        app = starlette.applications.Starlette(routes=self._routes())

        # configure cors
        if allowed_origins:
            app.add_middleware(
                starlette.middleware.cors.CORSMiddleware,
                allow_origins=allowed_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        super().__init__(app)

    def _routes(self):
        return [
            create_tileset_route(self._tilesets),
            create_resources_route(self._resources),
        ]

    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"

    def create(
        self,
        content: str = "",
        filepath: Optional[pathlib.Path] = None,
        tileset: Optional[Tileset] = None,
        headers: Optional[Dict[str, str]] = None,
        extension: Optional[str] = None,
        route: Optional[str] = None,
    ) -> Union[Resource, TilesetResource]:

        sources = sum(map(bool, (content, filepath, tileset)))
        if sources != 1:
            raise ValueError("Must provide exactly one of content, filepath, tileset")

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
            else:
                raise ValueError("Must provide one of content, filepath, or tileset.")

            self._resources[resource.guid] = resource

        self.start()
        return resource
