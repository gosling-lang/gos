from gosling.schema import Undefined, channels, core, mixins
from gosling.utils import infer_encoding_types
from gosling.display import JSRenderer  # , HTMLRenderer

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 180

# create alias for DataDeep type
Data = core.DataDeep

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


class Chart(core.Root):
    def _repr_mimebundle_(self, include=None, exclude=None):
        dct = self.to_dict()
        renderer = renderers.get("js")
        return renderer(dct) if renderer else {}

    def display(self):
        from IPython.display import display

        display(self)


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
            copy[key] = value
        return copy


class Track(_EncodingMixin, _PropertiesMixen, mixins.MarkMethodMixin, core.Track):
    def __init__(self, data=Undefined, **kwargs):
        super().__init__(
            data=data,
            width=kwargs.pop("width", DEFAULT_WIDTH),
            height=kwargs.pop("height", DEFAULT_HEIGHT),
            **kwargs,
        )

    def chart(self, **kwargs):
        return Chart(tracks=[self.copy()], **kwargs)


class PartialTrack(
    _EncodingMixin, _PropertiesMixen, mixins.MarkMethodMixin, core.PartialTrack
):
    ...
