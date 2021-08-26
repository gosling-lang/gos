from typing import TypeVar
from gosling.schema import Undefined, channels, core, mixins
from gosling.utils import infer_encoding_types
from gosling.display import JSRenderer  # , HTMLRenderer

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 180
DEFAULT_MARK = "bar"

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

T = TypeVar("T")

# Aliases & Utils
Data = core.DataDeep


def value(value, **kwargs):
    return dict(value=value, **kwargs)


class _EncodingMixin:
    def encode(self: T, *args, **kwargs) -> T:
        # Convert args to kwargs based on their types.
        copy = self.copy()
        kwargs = infer_encoding_types(args, kwargs, channels)
        for key, value in kwargs.items():
            copy[key] = value
        return copy


class _PropertiesMixen:
    def properties(self: T, **kwargs) -> T:
        copy = self.copy()
        for key, value in kwargs.items():
            setattr(copy, key, value)
        return copy


class _TransformsMixen:
    def _add_transform(self: T, *transforms) -> T:
        copy = self.copy()
        if copy.dataTransform is Undefined:
            copy.dataTransform = []
        copy.dataTransform.extend(transforms)
        return copy

    def transform_filter(self: T, field, **kwargs) -> T:
        return self._add_transform(
            core.FilterTransform(type="filter", field=field, **kwargs)
        )

    def transform_filter_not(self: T, field, **kwargs) -> T:
        kwargs["not"] = True
        return self._add_transform(
            core.FilterTransform(type="filter", field=field, **kwargs)
        )

    def transform_log(self: T, field, **kwargs) -> T:
        return self._add_transform(
            core.LogTransform(type="log", field=field, **kwargs),
        )

    def transform_str_concat(self: T, fields, **kwargs) -> T:
        return self._add_transform(
            core.StrConcatTransform(type="concat", fields=fields, **kwargs),
        )

    def transform_str_replace(self: T, field, **kwargs) -> T:
        return self._add_transform(
            core.StrReplaceTransform(type="replace", field=field, **kwargs)
        )

    def transform_displace(self: T, **kwargs) -> T:
        return self._add_transform(core.DisplaceTransform(type="displace", **kwargs))

    def transform_exon_split(self: T, **kwargs) -> T:
        return self._add_transform(core.ExonSplitTransform(type="exonSplit", **kwargs))

    def transform_coverage(self: T, startField, endField, **kwargs) -> T:
        return self._add_transform(
            core.CoverageTransform(
                type="coverage", startField=startField, endField=endField, **kwargs
            )
        )

    def transform_json_parse(self: T, field, **kwargs) -> T:
        return self._add_transform(
            core.JSONParseTransform(type="subjson", field=field, **kwargs)
        )


class View(_PropertiesMixen, core.Root):
    def _repr_mimebundle_(self, include=None, exclude=None):
        dct = self.to_dict()
        renderer = renderers.get("js")
        return renderer(dct) if renderer else {}

    def display(self):
        from IPython.display import display

        display(self)


def _auto_cast_to_view(views):
    """Converts a list of Tracks and/or Views into a list of Views."""
    return [v.view() if isinstance(v, Track) else v for v in views]


def horizontal(*views, **kwargs):
    views = _auto_cast_to_view(views)
    return View(arrangement="horizontal", views=views, **kwargs)


def vertical(*views, **kwargs):
    views = _auto_cast_to_view(views)
    return View(arrangement="vertical", views=views, **kwargs)


def parallel(*views, **kwargs):
    views = _auto_cast_to_view(views)
    return View(arrangement="parallel", views=views, **kwargs)


def serial(*views, **kwargs):
    views = _auto_cast_to_view(views)
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


class Track(
    _EncodingMixin,
    _PropertiesMixen,
    _TransformsMixen,
    mixins.MarkMethodMixin,
    core.SingleTrack,
):
    def __init__(self, data=Undefined, **kwargs):
        super().__init__(
            data=data,
            width=kwargs.pop("width", DEFAULT_WIDTH),
            height=kwargs.pop("height", DEFAULT_HEIGHT),
            mark=kwargs.pop("mark", DEFAULT_MARK),
            **kwargs,
        )

    def view(self, **kwargs):
        return View(tracks=[self], **kwargs)
