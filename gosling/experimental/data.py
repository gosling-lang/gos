import pathlib
from typing import Callable, Optional, Union

import gosling.experimental._tilesets as tilesets
from gosling.experimental._provider import Provider, Resource, TilesetResource
from gosling.utils.core import _compute_data_hash


def _hash_path(path: pathlib.Path):
    return _compute_data_hash(str(path))


class GoslingDataServer:
    """Backend server for Gosling datasets."""

    def __init__(self) -> None:
        self._provider: Optional[Provider] = None
        # We need to keep references to served resources, because the background
        # server uses weakrefs.
        self._resources: dict[str, Union[Resource, TilesetResource]] = {}

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
        self, data: Union[pathlib.Path, tilesets.Tileset], port: Optional[int] = None
    ):
        if self._provider is None:
            self._provider = Provider(allowed_origins=["*"]).start(port=port)

        if port is not None and port != self._provider.port:
            self._provider.stop().start(port=port)

        if isinstance(data, tilesets.Tileset):
            key = "tileset"
            path = data.filepath
        else:
            key = "filepath"
            path = data

        resource_id = _hash_path(path)
        if resource_id not in self._resources:
            self._resources[resource_id] = self._provider.create(**{key: data})

        return self._resources[resource_id].url

    def __rich_repr__(self):
        yield "resources", self._resources
        yield "port", self.port


data_server = GoslingDataServer()


def _create_loader(
    type_: str, tileset_cls: Optional[Callable[[pathlib.Path], tilesets.Tileset]] = None
):
    def load(url, **kwargs):
        fp = pathlib.Path(url)
        if fp.is_file():
            data = tileset_cls(fp) if tileset_cls else fp
            url = data_server(data)
        return dict(type=type_, url=url, **kwargs)

    return load


# file resources
csv = _create_loader("csv")
json = _create_loader("json")
bigwig = _create_loader("bigwig")

# tileset resources
bam = _create_loader("bam", tilesets.bam)
beddb = _create_loader("beddb", tilesets.beddb)
vector = _create_loader("vector", tilesets.bigwig)
matrix = _create_loader("matrix", tilesets.cooler)
multivec = _create_loader("multivec", tilesets.multivec)
