import pathlib


def iter_examples():
    example_dir = pathlib.Path(__file__).parent.absolute()
    for fp in example_dir.iterdir():
        if fp.name.startswith("_") or fp.suffix != ".py":
            continue
        yield fp
