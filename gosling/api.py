from gosling.schema import Undefined, channels, core, mixins
from gosling.utils import infer_encoding_types
from gosling.display import JSRenderer  # , HTMLRenderer

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 180

renderers = {
    # "html": HTMLRenderer(
    #     gosling_version=GOSLING_VERSION,
    #     higlass_version=HIGLASS_VERSION,
    #     react_version=REACT_VERSION,
    #     react_dom_version=REACT_DOM_VERSION,
    #     pixijs_version=PIXIJS_VERSION,
    # ),
    "js": JSRenderer(),
}

# Aliases & Utils
Data = core.DataDeep

def value(value, **kwargs):
    return dict(value=value, **kwargs)


class _EncodingMixin:
    def encode(self, *args, **kwargs):
        # Convert args to kwargs based on their types.
        copy = self.copy()
        kwargs = infer_encoding_types(args, kwargs, channels)
        for key, value in kwargs.items():
            copy[key] = value
        return copy


class _PropertiesMixen:
    def properties(self, **kwargs):
        copy = self.copy()
        for key, value in kwargs.items():
            setattr(copy, key, value)
        return copy


class View(_PropertiesMixen, core.Root):
    def _repr_mimebundle_(self, include=None, exclude=None):
        dct = self.to_dict()
        renderer = renderers.get("js")
        return renderer(dct) if renderer else {}

    def display(self):
        from IPython.display import display

        display(self)


def horizontal(*views, **kwargs):
    return View(arrangement="horizontal", views=views, **kwargs)


def vertical(*views, **kwargs):
    return View(arrangement="vertical", views=views, **kwargs)


def parallel(*views, **kwargs):
    return View(arrangement="parallel", views=views, **kwargs)


def serial(*views, **kwargs):
    return View(arrangement="serial", views=views, **kwargs)


# View utilities


def overlay(*tracks, **kwargs):
    """Compose an overlaid view from multiple tracks or overliad tracks."""
    # Overlay requires a `width` and `height`. Check if provided as kwargs, otherwise
    # eagerly grab the width/height from the tracks, otherwise use defaults.
    width = kwargs.pop(
        "width", next((t.width for t in tracks if t.width != Undefined), DEFAULT_WIDTH)
    )

    height = kwargs.pop(
        "height",
        next((t.height for t in tracks if t.height != Undefined), DEFAULT_HEIGHT),
    )

    # TODO: Gosling.js doesn't respect the parent width/height if defined in children.
    # This is a hack to ensure the children respect the view-level config.
    tracks = [t.properties(width=Undefined, height=Undefined) for t in tracks]

    return View(
        alignment="overlay", tracks=tracks, width=width, height=height, **kwargs
    )


def stack(*tracks, **kwargs):
    """Compose a stacked view from multiple tracks or overlaid tracks."""
    return View(alignment="stack", tracks=tracks, **kwargs)


class Track(_EncodingMixin, _PropertiesMixen, mixins.MarkMethodMixin, core.Track):
    def __init__(self, data=Undefined, **kwargs):
        super().__init__(
            data=data,
            width=kwargs.pop("width", DEFAULT_WIDTH),
            height=kwargs.pop("height", DEFAULT_HEIGHT),
            **kwargs,
        )

    def view(self, **kwargs):
        return View(tracks=[self], **kwargs)
