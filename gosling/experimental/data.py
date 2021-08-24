import pathlib
from typing import Optional, Union

import gosling.data as url_loaders
import gosling.experimental._tilesets as tilesets
from gosling.experimental._provider import Provider, Resource, TilesetResource
from gosling.utils.core import _compute_data_hash


def _hash_filepath(path: pathlib.Path):
    return _compute_data_hash(str(path))


def _with_default(url_loader):
    """Delegates data creation method based on whether path is url or local file."""

    def decorator(file_loader):
        def wrapper(*args, **kwargs):
            if "url" in kwargs and "filepath" in kwargs:
                raise ValueError("Must provide one of url or filepath")

            if "url" in kwargs:
                return url_loader(*args, **kwargs)

            if "filepath" in kwargs:
                # Ensure path is a Path
                filepath = pathlib.Path(kwargs.pop("filepath"))
                return file_loader(filepath=filepath, **kwargs)

            if len(args) != 1:
                raise ValueError(
                    "Can only provide url or filepath as positional argument."
                )

            if args[0] in {"http://", "https://"}:
                return url_loader(*args, **kwargs)

            # Try to read as file
            filepath = pathlib.Path(args[0])
            assert filepath.is_file()
            return file_loader(filepath=filepath, **kwargs)

        return wrapper

    return decorator


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

    def __call__(
        self, data: Union[pathlib.Path, tilesets.Tileset], port: Optional[int] = None
    ):
        if self._provider is None:
            self._provider = Provider(allowed_origins=["*"]).start(port=port)

        if port is not None and port != self._provider.port:
            self._provider.stop().start(port=port)

        if isinstance(data, tilesets.Tileset):
            resource_id = data.guid
            if data.guid not in self._resources:
                self._resources[resource_id] = self._provider.create(tileset=data)
        else:
            resource_id = _hash_filepath(data)
            if resource_id not in self._resources:
                self._resources[resource_id] = self._provider.create(filepath=data)

        return self._resources[resource_id].url


data_server = GoslingDataServer()


@_with_default(url_loaders.csv)
def csv(filepath: pathlib.Path, **kwargs):
    return dict(type="csv", url=data_server(filepath), **kwargs)


@_with_default(url_loaders.json)
def json(filepath: pathlib.Path, **kwargs):
    return dict(type="json", url=data_server(filepath), **kwargs)


@_with_default(url_loaders.bigwig)
def bigwig(filepath: pathlib.Path, **kwargs):
    return dict(type="bigwig", url=data_server(filepath), **kwargs)


@_with_default(url_loaders.beddb)
def beddb(filepath: pathlib.Path, **kwargs):
    tileset = tilesets.beddb(filepath, guid=_hash_filepath(filepath))
    return dict(type="beddb", url=data_server(tileset), **kwargs)


@_with_default(url_loaders.vector)
def vector(filepath: pathlib.Path, **kwargs):
    tileset = tilesets.bigwig(filepath, guid=_hash_filepath(filepath))
    return dict(type="vector", url=data_server(tileset), **kwargs)


@_with_default(url_loaders.multivec)
def multivec(filepath: pathlib.Path, **kwargs):
    tileset = tilesets.multivec(filepath, guid=_hash_filepath(filepath))
    return dict(type="multivec", url=data_server(tileset), **kwargs)


@_with_default(url_loaders.bam)
def bam(filepath: pathlib.Path, **kwargs):
    tileset = tilesets.bam(filepath, guid=_hash_filepath(filepath))
    return dict(type="bam", url=data_server(tileset), **kwargs)


@_with_default(url_loaders.matrix)
def matrix(filepath: pathlib.Path, **kwargs):
    tileset = tilesets.cooler(filepath, guid=_hash_filepath(filepath))
    return dict(type="matrix", url=data_server(tileset), **kwargs)
