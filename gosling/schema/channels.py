# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.

from . import core
from gosling.schemapi import Undefined
import gosling.utils as utils


class FieldChannelMixin(object):
    def to_dict(self, validate=True, ignore=(), context=None):
        context = context or {}
        shorthand = self._get('shorthand')
        field = self._get('field')

        if shorthand is not Undefined and field is not Undefined:
            raise ValueError("{} specifies both shorthand={} and field={}. "
                             "".format(self.__class__.__name__, shorthand, field))

        if isinstance(shorthand, (tuple, list)):
            # If given a list of shorthands, then transform it to a list of classes
            kwds = self._kwds.copy()
            kwds.pop('shorthand')
            return [self.__class__(sh, **kwds).to_dict(validate=validate, ignore=ignore, context=context)
                    for sh in shorthand]

        if shorthand is Undefined:
            parsed = {}
        elif isinstance(shorthand, str):
            parsed = utils.parse_shorthand(shorthand)
            type_required = 'type' in self._kwds
            type_in_shorthand = 'type' in parsed
            type_defined_explicitly = self._get('type') is not Undefined
            if not (type_in_shorthand or type_defined_explicitly):
                raise ValueError("{} encoding field is specified without a type; "
                                 "the type cannot be automatically inferred because "
                                 "the data is not specified as a pandas.DataFrame."
                                 "".format(shorthand))
        else:
            # Shorthand is not a string; we pass the definition to field,
            # and do not do any parsing.
            parsed = {'field': shorthand}

        # Set shorthand to Undefined, because it's not part of the base schema.
        self.shorthand = Undefined
        self._kwds.update({k: v for k, v in parsed.items()
                           if self._get(k) is Undefined})
        return super(FieldChannelMixin, self).to_dict(
            validate=validate,
            ignore=ignore,
            context=context
        )


class ValueChannelMixin(object):
    def to_dict(self, validate=True, ignore=(), context=None):
        context = context or {}
        condition = getattr(self, 'condition', Undefined)
        copy = self  # don't copy unless we need to
        if condition is not Undefined:
            if isinstance(condition, core.SchemaBase):
                pass
            elif 'field' in condition and 'type' not in condition:
                kwds = parse_shorthand(condition['field'], context.get('data', None))
                copy = self.copy(deep=['condition'])
                copy.condition.update(kwds)
        return super(ValueChannelMixin, copy).to_dict(validate=validate,
                                                      ignore=ignore,
                                                      context=context)


class Color(FieldChannelMixin, core.Color):
    """Color schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    legend : boolean
        Whether to display legend. __Default__: `false`
    range : :class:`Range`
        Determine the colors that should be bound to data value. Default properties are
        determined considering the field type.
    scale : enum('linear', 'log')

    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "color"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, legend=Undefined,
                 range=Undefined, scale=Undefined, type=Undefined, **kwds):
        super(Color, self).__init__(shorthand=shorthand, domain=domain, field=field, legend=legend,
                                    range=range, scale=scale, type=type, **kwds)


class ColorValue(ValueChannelMixin, core.ChannelValue):
    """ColorValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "color"

    def __init__(self, value, **kwds):
        super(ColorValue, self).__init__(value=value, **kwds)


class Opacity(FieldChannelMixin, core.Opacity):
    """Opacity schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "opacity"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, range=Undefined,
                 type=Undefined, **kwds):
        super(Opacity, self).__init__(shorthand=shorthand, domain=domain, field=field, range=range,
                                      type=type, **kwds)


class OpacityValue(ValueChannelMixin, core.ChannelValue):
    """OpacityValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "opacity"

    def __init__(self, value, **kwds):
        super(OpacityValue, self).__init__(value=value, **kwds)


class Row(FieldChannelMixin, core.Row):
    """Row schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    padding : float
        Determines the size of inner white spaces on the top and bottom of individiual rows.
        __Default__: `0`
    range : :class:`ValueExtent`
        Determine the start and end position of rendering area of this track along vertical
        axis. __Default__: `[0, height]`
    type : string
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "row"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, grid=Undefined,
                 legend=Undefined, padding=Undefined, range=Undefined, type=Undefined, **kwds):
        super(Row, self).__init__(shorthand=shorthand, domain=domain, field=field, grid=grid,
                                  legend=legend, padding=padding, range=range, type=type, **kwds)


class RowValue(ValueChannelMixin, core.ChannelValue):
    """RowValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "row"

    def __init__(self, value, **kwds):
        super(RowValue, self).__init__(value=value, **kwds)


class Size(FieldChannelMixin, core.Size):
    """Size schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    legend : boolean
        not supported: Whether to display legend. __Default__: `false`
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "size"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, legend=Undefined,
                 range=Undefined, type=Undefined, **kwds):
        super(Size, self).__init__(shorthand=shorthand, domain=domain, field=field, legend=legend,
                                   range=range, type=type, **kwds)


class SizeValue(ValueChannelMixin, core.ChannelValue):
    """SizeValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "size"

    def __init__(self, value, **kwds):
        super(SizeValue, self).__init__(value=value, **kwds)


class Stroke(FieldChannelMixin, core.Stroke):
    """Stroke schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`Range`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "stroke"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, range=Undefined,
                 type=Undefined, **kwds):
        super(Stroke, self).__init__(shorthand=shorthand, domain=domain, field=field, range=range,
                                     type=type, **kwds)


class StrokeValue(ValueChannelMixin, core.ChannelValue):
    """StrokeValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "stroke"

    def __init__(self, value, **kwds):
        super(StrokeValue, self).__init__(value=value, **kwds)


class StrokeWidth(FieldChannelMixin, core.StrokeWidth):
    """StrokeWidth schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : :class:`ValueExtent`
        Values of the data
    field : string
        Name of the data field
    range : :class:`ValueExtent`
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "strokeWidth"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, range=Undefined,
                 type=Undefined, **kwds):
        super(StrokeWidth, self).__init__(shorthand=shorthand, domain=domain, field=field, range=range,
                                          type=type, **kwds)


class StrokeWidthValue(ValueChannelMixin, core.ChannelValue):
    """StrokeWidthValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "strokeWidth"

    def __init__(self, value, **kwds):
        super(StrokeWidthValue, self).__init__(value=value, **kwds)


class Text(FieldChannelMixin, core.Text):
    """Text schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    domain : List(string)
        Values of the data
    field : string
        Name of the data field
    range : List(string)
        Ranges of visual channel values
    type : enum('quantitative', 'nominal')
        Specify the data type
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "text"

    def __init__(self, shorthand=Undefined, domain=Undefined, field=Undefined, range=Undefined,
                 type=Undefined, **kwds):
        super(Text, self).__init__(shorthand=shorthand, domain=domain, field=field, range=range,
                                   type=type, **kwds)


class TextValue(ValueChannelMixin, core.ChannelValue):
    """TextValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "text"

    def __init__(self, value, **kwds):
        super(TextValue, self).__init__(value=value, **kwds)


class X(FieldChannelMixin, core.X):
    """X schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    domain : :class:`GenomicDomain`
        Values of the data
    field : string
        Name of the data field.
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : string
        Specify the data type.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, domain=Undefined,
                 field=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 range=Undefined, type=Undefined, **kwds):
        super(X, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, domain=domain,
                                field=field, grid=grid, legend=legend, linkingId=linkingId, range=range,
                                type=type, **kwds)


class XValue(ValueChannelMixin, core.ChannelValue):
    """XValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x"

    def __init__(self, value, **kwds):
        super(XValue, self).__init__(value=value, **kwds)


class X1(FieldChannelMixin, core.X):
    """X1 schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    domain : :class:`GenomicDomain`
        Values of the data
    field : string
        Name of the data field.
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : string
        Specify the data type.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x1"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, domain=Undefined,
                 field=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 range=Undefined, type=Undefined, **kwds):
        super(X1, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, domain=domain,
                                 field=field, grid=grid, legend=legend, linkingId=linkingId,
                                 range=range, type=type, **kwds)


class X1Value(ValueChannelMixin, core.ChannelValue):
    """X1Value schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x1"

    def __init__(self, value, **kwds):
        super(X1Value, self).__init__(value=value, **kwds)


class X1e(FieldChannelMixin, core.X):
    """X1e schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    domain : :class:`GenomicDomain`
        Values of the data
    field : string
        Name of the data field.
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : string
        Specify the data type.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x1e"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, domain=Undefined,
                 field=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 range=Undefined, type=Undefined, **kwds):
        super(X1e, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, domain=domain,
                                  field=field, grid=grid, legend=legend, linkingId=linkingId,
                                  range=range, type=type, **kwds)


class X1eValue(ValueChannelMixin, core.ChannelValue):
    """X1eValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "x1e"

    def __init__(self, value, **kwds):
        super(X1eValue, self).__init__(value=value, **kwds)


class Xe(FieldChannelMixin, core.X):
    """Xe schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    domain : :class:`GenomicDomain`
        Values of the data
    field : string
        Name of the data field.
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : string
        Specify the data type.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "xe"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, domain=Undefined,
                 field=Undefined, grid=Undefined, legend=Undefined, linkingId=Undefined,
                 range=Undefined, type=Undefined, **kwds):
        super(Xe, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, domain=domain,
                                 field=field, grid=grid, legend=legend, linkingId=linkingId,
                                 range=range, type=type, **kwds)


class XeValue(ValueChannelMixin, core.ChannelValue):
    """XeValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "xe"

    def __init__(self, value, **kwds):
        super(XeValue, self).__init__(value=value, **kwds)


class Y(FieldChannelMixin, core.Y):
    """Y schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    baseline : anyOf(string, float)
        Custom baseline of the y-axis. __Default__: `0`
    domain : anyOf(:class:`ValueExtent`, :class:`GenomicDomain`)
        Values of the data
    field : string
        Name of the data field.
    flip : boolean
        Whether to flip the y-axis. This is done by inverting the `range` property.
        __Default__: `false`
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : enum('quantitative', 'nominal', 'genomic')
        Specify the data type.
    zeroBaseline : boolean
        Specify whether to use zero baseline. __Default__: `true`
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, baseline=Undefined,
                 domain=Undefined, field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined,
                 linkingId=Undefined, range=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Y, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, baseline=baseline,
                                domain=domain, field=field, flip=flip, grid=grid, legend=legend,
                                linkingId=linkingId, range=range, type=type, zeroBaseline=zeroBaseline,
                                **kwds)


class YValue(ValueChannelMixin, core.ChannelValue):
    """YValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y"

    def __init__(self, value, **kwds):
        super(YValue, self).__init__(value=value, **kwds)


class Y1(FieldChannelMixin, core.Y):
    """Y1 schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    baseline : anyOf(string, float)
        Custom baseline of the y-axis. __Default__: `0`
    domain : anyOf(:class:`ValueExtent`, :class:`GenomicDomain`)
        Values of the data
    field : string
        Name of the data field.
    flip : boolean
        Whether to flip the y-axis. This is done by inverting the `range` property.
        __Default__: `false`
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : enum('quantitative', 'nominal', 'genomic')
        Specify the data type.
    zeroBaseline : boolean
        Specify whether to use zero baseline. __Default__: `true`
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y1"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, baseline=Undefined,
                 domain=Undefined, field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined,
                 linkingId=Undefined, range=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Y1, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, baseline=baseline,
                                 domain=domain, field=field, flip=flip, grid=grid, legend=legend,
                                 linkingId=linkingId, range=range, type=type, zeroBaseline=zeroBaseline,
                                 **kwds)


class Y1Value(ValueChannelMixin, core.ChannelValue):
    """Y1Value schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y1"

    def __init__(self, value, **kwds):
        super(Y1Value, self).__init__(value=value, **kwds)


class Y1e(FieldChannelMixin, core.Y):
    """Y1e schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    baseline : anyOf(string, float)
        Custom baseline of the y-axis. __Default__: `0`
    domain : anyOf(:class:`ValueExtent`, :class:`GenomicDomain`)
        Values of the data
    field : string
        Name of the data field.
    flip : boolean
        Whether to flip the y-axis. This is done by inverting the `range` property.
        __Default__: `false`
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : enum('quantitative', 'nominal', 'genomic')
        Specify the data type.
    zeroBaseline : boolean
        Specify whether to use zero baseline. __Default__: `true`
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y1e"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, baseline=Undefined,
                 domain=Undefined, field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined,
                 linkingId=Undefined, range=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Y1e, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis,
                                  baseline=baseline, domain=domain, field=field, flip=flip, grid=grid,
                                  legend=legend, linkingId=linkingId, range=range, type=type,
                                  zeroBaseline=zeroBaseline, **kwds)


class Y1eValue(ValueChannelMixin, core.ChannelValue):
    """Y1eValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "y1e"

    def __init__(self, value, **kwds):
        super(Y1eValue, self).__init__(value=value, **kwds)


class Ye(FieldChannelMixin, core.Y):
    """Ye schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`
        Specify how to aggregate data. __Default__: `undefined`
    axis : :class:`AxisPosition`
        Specify where should the axis be put
    baseline : anyOf(string, float)
        Custom baseline of the y-axis. __Default__: `0`
    domain : anyOf(:class:`ValueExtent`, :class:`GenomicDomain`)
        Values of the data
    field : string
        Name of the data field.
    flip : boolean
        Whether to flip the y-axis. This is done by inverting the `range` property.
        __Default__: `false`
    grid : boolean
        Whether to display grid. __Default__: `false`
    legend : boolean
        Whether to display legend. __Default__: `false`
    linkingId : string
        Users need to assign a unique linkingId for [linking
        views](/docs/user-interaction#linking-views) and [Brushing and
        Linking](/docs/user-interaction#brushing-and-linking)
    range : :class:`ValueExtent`
        Values of the visual channel.
    type : enum('quantitative', 'nominal', 'genomic')
        Specify the data type.
    zeroBaseline : boolean
        Specify whether to use zero baseline. __Default__: `true`
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "ye"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, baseline=Undefined,
                 domain=Undefined, field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined,
                 linkingId=Undefined, range=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Ye, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis, baseline=baseline,
                                 domain=domain, field=field, flip=flip, grid=grid, legend=legend,
                                 linkingId=linkingId, range=range, type=type, zeroBaseline=zeroBaseline,
                                 **kwds)


class YeValue(ValueChannelMixin, core.ChannelValue):
    """YeValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)
        Assign a constant value for a visual channel.
    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "ye"

    def __init__(self, value, **kwds):
        super(YeValue, self).__init__(value=value, **kwds)
