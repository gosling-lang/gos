from __future__ import annotations

import functools
import pathlib
import typing
from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class Tileset:
    filepath: pathlib.Path
    tiles_impl: typing.Callable[[typing.Sequence[str]], list[typing.Any]]
    info: typing.Callable[[], typing.Any]
    uid: str
    type: None | str = None

    def tiles(self, tile_ids: typing.Sequence[str]) -> list[typing.Any]:
        return self.tiles_impl(tile_ids)


def create_uid(filepath: pathlib.Path) -> str:
    return hashlib.md5(str(filepath).encode()).hexdigest()[0:8]


def beddb(filepath: pathlib.Path):
    try:
        from clodius.tiles.beddb import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "beddb" data-server.'
        )

    return Tileset(
        filepath=filepath,
        type="beddb",
        tiles_impl=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=create_uid(filepath),
    )


def bigwig(filepath: pathlib.Path):
    try:
        from clodius.tiles.bigwig import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "vector" data-server.'
        )

    return Tileset(
        filepath=filepath,
        type="bigwig",
        tiles_impl=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=create_uid(filepath),
    )


def multivec(filepath: pathlib.Path):
    try:
        from clodius.tiles.multivec import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "multivec" data-server.'
        )

    return Tileset(
        filepath=filepath,
        type="multivec",
        tiles_impl=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=create_uid(filepath),
    )


def cooler(filepath: pathlib.Path):
    try:
        from clodius.tiles.cooler import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "matrix" data-server.'
        )

    return Tileset(
        filepath=filepath,
        type="cooler",
        tiles_impl=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        uid=create_uid(filepath),
    )
