from __future__ import annotations

import functools
import pathlib
import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Tileset:
    filepath: pathlib.Path
    tiles: typing.Callable[[typing.Sequence[str]], list[typing.Any]]
    info: typing.Callable[[], typing.Any]
    type: None | str = None


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
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
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
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
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
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
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
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
    )
