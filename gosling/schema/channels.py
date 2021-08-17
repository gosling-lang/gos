# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.

from . import core
from gosling.schemapi import Undefined
from gosling.utils import parse_shorthand


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
            parsed = parse_shorthand(shorthand)
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


class Channel(FieldChannelMixin, core.ChannelDeep):
    """Channel schema wrapper

    Mapping(required=[shorthand])

    Attributes
    ----------

    shorthand : string
        shorthand for field, aggregate, and type
    aggregate : :class:`Aggregate`

    axis : :class:`AxisPosition`

    baseline : anyOf(string, float)

    domain : :class:`Domain`

    field : string

    flip : boolean

    grid : boolean

    legend : boolean

    linkingId : string

    mirrored : boolean

    padding : float

    range : :class:`Range`

    sort : List(string)

    stack : boolean

    type : :class:`FieldType`

    zeroBaseline : boolean

    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "Channel"

    def __init__(self, shorthand=Undefined, aggregate=Undefined, axis=Undefined, baseline=Undefined,
                 domain=Undefined, field=Undefined, flip=Undefined, grid=Undefined, legend=Undefined,
                 linkingId=Undefined, mirrored=Undefined, padding=Undefined, range=Undefined,
                 sort=Undefined, stack=Undefined, type=Undefined, zeroBaseline=Undefined, **kwds):
        super(Channel, self).__init__(shorthand=shorthand, aggregate=aggregate, axis=axis,
                                      baseline=baseline, domain=domain, field=field, flip=flip,
                                      grid=grid, legend=legend, linkingId=linkingId, mirrored=mirrored,
                                      padding=padding, range=range, sort=sort, stack=stack, type=type,
                                      zeroBaseline=zeroBaseline, **kwds)


class ChannelValue(ValueChannelMixin, core.ChannelValue):
    """ChannelValue schema wrapper

    Mapping(required=[value])

    Attributes
    ----------

    value : anyOf(float, string)

    """
    _class_is_valid_at_instantiation = False
    _encoding_name = "Channel"

    def __init__(self, value, **kwds):
        super(ChannelValue, self).__init__(value=value, **kwds)
