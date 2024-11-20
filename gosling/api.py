import pathlib
from typing import Iterable, TypeVar, Union, Literal

import gosling.display as display
import gosling.utils as utils
from gosling.schema import Undefined, channels, core, mixins

DEFAULT_MARK = "bar"

T = TypeVar("T")

# Aliases & Utils
Data = core.DataDeep


def value(value, **kwargs):
    """Specify a value for use in an encoding"""
    return dict(value=value, **kwargs)


class _EncodingMixin:
    def encode(self: T, *args, **kwargs) -> T:
        """
        Add channel encodings to the track.

        Parameters
        ----------
        column : :class:`Column`

        opacity : :class:`Opacity`

        row : :class:`Row`

        size : :class:`Size`

        stroke : :class:`Stroke`

        strokeWidth : :class:`StrokeWidth`

        text : :class:`Text`

        x : :class:`X`

        x1 : :class:`X1`

        x1e : :class:`X1e`

        xe : :class:`Xe`

        y : :class:`Y`

        y1 : :class:`Y1`

        y1e : :class:`Y1e`

        ye : :class:`Ye`
        """
        # Convert args to kwargs based on their types.
        copy = self.copy()
        kwargs = utils.infer_encoding_types(args, kwargs, channels)
        for key, value in kwargs.items():
            copy[key] = value
        return copy


class _PropertiesMixin:
    def properties(self: T, **kwargs) -> T:
        """Set top-level properties of the View or Track.

        Argument names and types are the same as class initialization.
        """
        copy = self.copy()
        for key, value in kwargs.items():
            setattr(copy, key, value)
        return copy


class _TransformsMixin:
    def _add_transform(self: T, *transforms) -> T:
        copy = self.copy()
        if copy.dataTransform is Undefined:
            copy.dataTransform = []
        copy.dataTransform.extend(transforms)
        return copy

    @utils.use_signature(core.FilterTransform)
    def transform_filter(self: T, field, **kwargs) -> T:
        """Add FilterTransform to Track"""
        return self._add_transform(
            core.FilterTransform(type="filter", field=field, **kwargs)
        )

    @utils.use_signature(core.FilterTransform)
    def transform_filter_not(self: T, field, **kwargs) -> T:
        """Add FilterTransform with `not=True` to Track"""
        kwargs["not"] = True
        return self._add_transform(
            core.FilterTransform(type="filter", field=field, **kwargs)
        )

    @utils.use_signature(core.LogTransform)
    def transform_log(self: T, field, **kwargs) -> T:
        """Add LogTransform to Track"""
        return self._add_transform(
            core.LogTransform(type="log", field=field, **kwargs),
        )

    @utils.use_signature(core.StrConcatTransform)
    def transform_str_concat(self: T, fields, **kwargs) -> T:
        """Add StrConcatTransform to Track"""
        return self._add_transform(
            core.StrConcatTransform(type="concat", fields=fields, **kwargs),
        )

    @utils.use_signature(core.StrReplaceTransform)
    def transform_str_replace(self: T, field, **kwargs) -> T:
        """Add StrReplaceTransform to Track"""
        return self._add_transform(
            core.StrReplaceTransform(type="replace", field=field, **kwargs)
        )

    @utils.use_signature(core.DisplaceTransform)
    def transform_displace(self: T, **kwargs) -> T:
        """Add DisplaceTransform to Track"""
        return self._add_transform(core.DisplaceTransform(type="displace", **kwargs))

    @utils.use_signature(core.ExonSplitTransform)
    def transform_exon_split(self: T, **kwargs) -> T:
        """Add ExonSplitTransform to Track"""
        return self._add_transform(core.ExonSplitTransform(type="exonSplit", **kwargs))

    @utils.use_signature(core.CoverageTransform)
    def transform_coverage(self: T, startField, endField, **kwargs) -> T:
        """Add CoverageTransform to Track"""
        return self._add_transform(
            core.CoverageTransform(
                type="coverage", startField=startField, endField=endField, **kwargs
            )
        )

    @utils.use_signature(core.JsonParseTransform)
    def transform_json_parse(self: T, field, **kwargs) -> T:
        """Add JSONParseTransform to Track"""
        return self._add_transform(
            core.JsonParseTransform(type="subjson", field=field, **kwargs)
        )


class _VisibilityMixin:
    def _add_visibility(self: T, *visibilities) -> T:
        copy = self.copy()
        if copy.visibility is Undefined:
            copy.visibility = []
        copy.visibility.extend(visibilities)
        return copy

    @utils.use_signature(core.VisibilityCondition)
    def visibility_lt(self: T, **kwargs) -> T:
        """Add less-than VisibilityCondition to Track"""
        return self._add_visibility(core.VisibilityCondition(operation="LT", **kwargs))

    @utils.use_signature(core.VisibilityCondition)
    def visibility_gt(self: T, **kwargs) -> T:
        """Add greater-than VisibilityCondition to Track"""
        return self._add_visibility(core.VisibilityCondition(operation="GT", **kwargs))

    @utils.use_signature(core.VisibilityCondition)
    def visibility_le(self: T, **kwargs) -> T:
        """Add less-than-or-equal-to VisibilityCondition to Track"""
        return self._add_visibility(
            core.VisibilityCondition(operation="LTET", **kwargs)
        )

    @utils.use_signature(core.VisibilityCondition)
    def visibility_ge(self: T, **kwargs) -> T:
        """Add greater-than-or-equal-to VisibilityCondition to Track"""
        return self._add_visibility(
            core.VisibilityCondition(operation="GTET", **kwargs)
        )


@utils.use_signature(core.Root)
class View(_PropertiesMixin, core.Root):
    """Create a basic Gosling View."""

    def _repr_mimebundle_(self, include=None, exclude=None):
        render = display.renderers.get()
        return render(self.to_dict())

    def display(self):
        """Render top-level chart using IPython.display."""
        from IPython.display import display

        display(self)

    def save(
        self,
        path: Union[pathlib.Path, str],
        format: Union[Literal["json", "html"], None] = None,
        **kwargs,
    ):
        if format is None:
            suffix = pathlib.Path(path).suffix.lstrip(".")
            if suffix in ("json", "html"):
                format = suffix
            else:
                raise ValueError("must specify file format: ['html', 'json']")

        if format == "json":
            data = self.to_json(**kwargs)
        elif format == "html":
            data = display.spec_to_html(self.to_dict(), **kwargs)
        else:
            raise ValueError(f"unrecognized format: '{format}'")

        with open(path, mode="w") as f:
            f.write(data)

    def widget(self):
        try:
            from ._widget import GoslingWidget
        except ImportError:
            raise ImportError(
                "The 'gosling-widget' package is required to use the widget() method."
            )

        return GoslingWidget(self.to_dict())


# View utilities


class Track(
    _EncodingMixin,
    _PropertiesMixin,
    _TransformsMixin,
    _VisibilityMixin,
    mixins.MarkMethodMixin,
    core.SingleTrack,
):
    """Create a basic Gosling Track.

    Although it is possible to set all Track properties as constructor attributes,
    it is more idiomatic to use methods such as ``mark_point()``, ``encode()``,
    ``transform_filter()``, ``properties()``, etc.
    """

    @utils.use_signature(core.SingleTrack)
    def __init__(self, data=Undefined, **kwargs):
        super().__init__(
            data=data,
            mark=kwargs.pop("mark", DEFAULT_MARK),
            **kwargs,
        )

    @utils.use_signature(core.SingleView)
    def view(self, **kwargs) -> View:
        """Convert Track into top-level gos.View"""
        return View(tracks=[self], **kwargs)


def overlay(*tracks: Union[Track, View], **kwargs) -> View:
    """Compose an overlaid view from multiple tracks or overliad tracks"""
    return View(alignment="overlay", tracks=tracks, **kwargs)


def stack(*tracks: Union[Track, View], **kwargs) -> View:
    """Compose a stacked view from multiple tracks or overlaid tracks."""
    return View(alignment="stack", tracks=tracks, **kwargs)


def _auto_cast_to_view(views: Iterable[Union[View, Track]]):
    """Converts a list of Tracks and/or Views into a list of Views."""
    return tuple(v.view() if isinstance(v, Track) else v for v in views)


def horizontal(*views: Union[View, Track], **kwargs) -> View:
    """Arrange multiple views horizontally."""
    views = _auto_cast_to_view(views)
    return View(arrangement="horizontal", views=views, **kwargs)


def vertical(*views: Union[View, Track], **kwargs) -> View:
    """Arrange multiple views vertically."""
    views = _auto_cast_to_view(views)
    return View(arrangement="vertical", views=views, **kwargs)


def parallel(*views: Union[View, Track], **kwargs) -> View:
    """Arrange multiple views in parallel."""
    views = _auto_cast_to_view(views)
    return View(arrangement="parallel", views=views, **kwargs)


def serial(*views: Union[View, Track], **kwargs) -> View:
    """Arrange multiple views in serial."""
    views = _auto_cast_to_view(views)
    return View(arrangement="serial", views=views, **kwargs)
