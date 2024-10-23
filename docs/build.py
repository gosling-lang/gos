# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "furo",
#     "gosling",
#     "numpydoc>=1.5",
#     "sphinx>=6.0",
# ]
#
# [tool.uv.sources]
# gosling = { path = "../" }
# ///
import pathlib

from sphinx.application import Sphinx

SELF_DIR = pathlib.Path(__file__).parent


def main():
    app = Sphinx(
        srcdir=SELF_DIR,
        confdir=SELF_DIR,
        outdir=SELF_DIR / "dist",
        doctreedir=SELF_DIR / "dist" / ".doctrees",
        buildername="html",
    )

    app.build()


if __name__ == "__main__":
    main()
