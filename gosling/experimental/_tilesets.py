import functools
import pathlib
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional


@dataclass(frozen=True)
class Tileset:
    filepath: pathlib.Path
    tiles: Callable[[Iterable[str]], list]
    info: Callable[[], dict[str, Any]]
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


def bam(filepath: pathlib.Path, index_filename=None, chromsizes=None):
    try:
        from clodius.tiles.bam import tiles, tileset_info
    except ImportError:
        raise ImportError('You must have `clodius` installed to use "bam" data-server.')

    if not index_filename:
        index_filename = filepath.with_suffix(".bai")

    return Tileset(
        filepath=filepath,
        type="bam",
        tiles=functools.partial(
            tiles, filepath, index_filename=index_filename, chromsizes=chromsizes
        ),
        info=functools.partial(tileset_info, filepath, chromsizes=chromsizes),
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
