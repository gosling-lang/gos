import functools
import pathlib
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class Tileset:
    tiles: Callable[[Iterable[str]], list]
    info: Callable[[], dict[str, Any]]
    guid: str = field(default_factory=lambda: str(uuid.uuid4()))


def beddb(filepath: pathlib.Path, **kwargs):
    try:
        from clodius.tiles.beddb import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "beddb" data-server.'
        )

    return Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        **kwargs,
    )


def bigwig(filepath: pathlib.Path, **kwargs):
    try:
        from clodius.tiles.bigwig import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "vector" data-server.'
        )

    return Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        **kwargs,
    )


def multivec(filepath: pathlib.Path, **kwargs):
    try:
        from clodius.tiles.multivec import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "multivec" data-server.'
        )

    return Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        **kwargs,
    )


def bam(filepath: pathlib.Path, index_filename=None, chromsizes=None, **kwargs):
    try:
        from clodius.tiles.bam import tiles, tileset_info
    except ImportError:
        raise ImportError('You must have `clodius` installed to use "bam" data-server.')

    if not index_filename:
        index_filename = filepath.with_suffix(".bai")

    return Tileset(
        tiles=functools.partial(
            tiles, filepath, index_filename=index_filename, chromsizes=chromsizes
        ),
        info=functools.partial(tileset_info, filepath, chromsizes=chromsizes),
        **kwargs,
    )


def cooler(filepath: pathlib.Path, **kwargs):
    try:
        from clodius.tiles.cooler import tiles, tileset_info
    except ImportError:
        raise ImportError(
            'You must have `clodius` installed to use "matrix" data-server.'
        )

    return Tileset(
        tiles=functools.partial(tiles, filepath),
        info=functools.partial(tileset_info, filepath),
        **kwargs,
    )
