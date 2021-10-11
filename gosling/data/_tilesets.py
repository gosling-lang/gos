import functools
import pathlib
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Optional


@dataclass(frozen=True)
class Tileset:
    filepath: pathlib.Path
    tiles: Callable[[Iterable[str]], List]
    info: Callable[[], Any]
    type: Optional[str] = None


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
