from gosling.schema import *
from gosling.api import *
from gosling.display import renderers


def _jupyter_nbextension_paths():
    """Return metadata for the jupyter-gosling nbextension."""
    return [
        dict(
            section="notebook",
            # the path is relative to the `gosling` directory
            src="static",
            # directory in the `nbextension/` namespace
            dest="jupyter-gosling",
            # _also_ in the `nbextension/` namespace
            require="jupyter-gosling/index",
        )
    ]
