import pathlib
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

import gosling.data._tilesets as tilesets
from gosling.utils.core import _compute_data_hash

if TYPE_CHECKING:
    from gosling.data._provider import Provider, Resource, TilesetResource

def _hash_path(path: pathlib.Path):
    return _compute_data_hash(str(path))


class GoslingDataServer:
    """Backend server for Gosling datasets."""

    def __init__(self) -> None:
        self._provider: Optional[Provider] = None
        # We need to keep references to served resources, because the background
        # server uses weakrefs.
        self._resources: Dict[str, Union[Resource, TilesetResource]] = {}

    @property
    def port(self):
        if not self._provider:
            raise RuntimeError("Server not started.")
        return self._provider.port

    def reset(self) -> None:
        if self._provider is not None:
            self._provider.stop()
        self._resources = {}

    def __call__(
        self,
        data: Union[str, pathlib.Path, tilesets.Tileset],
        port: Optional[int] = None,
        **kwargs,
    ):
        if self._provider is None:
            # only try to import server dependencies when using server
            from gosling.data._provider import Provider
            self._provider = Provider(allowed_origins=["*"]).start(port=port)

        if port is not None and port != self._provider.port:
            self._provider.stop().start(port=port)

        if isinstance(data, tilesets.Tileset):
            kwargs["tileset"] = data
            resource_id = _hash_path(data.filepath)
        elif isinstance(data, pathlib.Path):
            kwargs["filepath"] = data
            resource_id = _hash_path(data)
        else:
            kwargs["content"] = data
            resource_id = _compute_data_hash(data)

        if resource_id not in self._resources:
            self._resources[resource_id] = self._provider.create(**kwargs)

        return self._resources[resource_id].url

    def __rich_repr__(self):
        yield "resources", self._resources
        try:
            port = self.port
        except RuntimeError:
            port = None
        yield "port", port


data_server = GoslingDataServer()

CreateTileset = Callable[[pathlib.Path], tilesets.Tileset]


def _create_loader(type_: str, create_ts: Optional[CreateTileset] = None):
    def load(url: Union[pathlib.Path, str], **kwargs):
        """Adds resource to data_server if local file is detected."""
        fp = pathlib.Path(url)
        if fp.is_file():
            data = create_ts(fp) if create_ts else fp
            url = data_server(data)

        # bam's index file url
        if "indexUrl" in kwargs:
            fp = pathlib.Path(kwargs["indexUrl"])
            if fp.is_file():
                kwargs["indexUrl"] = data_server(fp)

        return dict(type=type_, url=str(url), **kwargs)

    return load


# in-memory data
def json(values: List[Dict[str, Any]], **kwargs):
    return dict(type="json", values=values, **kwargs)


# file resources
bam = _create_loader("bam")
csv = _create_loader("csv")
bigwig = _create_loader("bigwig")

# tileset resources
beddb = _create_loader("beddb", tilesets.beddb)
vector = _create_loader("vector", tilesets.bigwig)
matrix = _create_loader("matrix", tilesets.cooler)
multivec = _create_loader("multivec", tilesets.multivec)
