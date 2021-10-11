import hashlib
import itertools
import re
from typing import Any, Callable, List, Optional

import jsonschema

from gosling.schemapi import SchemaBase

TYPECODE_MAP = {
    "quantitative": "Q",
    "genomic": "G",
    "nominal": "N",
}

INV_TYPECODE_MAP = {v: k for k, v in TYPECODE_MAP.items()}


def parse_shorthand(
    shorthand,
    parse_types=True,
):
    """
    >>> parse_shorthand('name') == {'field': 'name'}
    True
    >>> parse_shorthand('name:Q') == {'field': 'name', 'type': 'quantitative'}
    True
    >>> parse_shorthand('foo:G') == {'field': 'foo', 'type': 'genomic'}
    True
    >>> parse_shorthand('foo:N') == {'field': 'foo', 'type': 'nominal'}
    True
    """
    if not shorthand:
        return {}

    valid_typecodes = list(TYPECODE_MAP) + list(INV_TYPECODE_MAP)

    units = dict(
        field="(?P<field>.*)",
        type="(?P<type>{})".format("|".join(valid_typecodes)),
    )

    patterns = []
    patterns.extend([r"{field}"])

    if parse_types:
        patterns = list(itertools.chain(*((p + ":{type}", p) for p in patterns)))

    regexps = (
        re.compile(r"\A" + p.format(**units) + r"\Z", re.DOTALL) for p in patterns
    )

    # find matches depending on valid fields passed
    if isinstance(shorthand, dict):
        attrs = shorthand
    else:
        attrs = next(
            exp.match(shorthand).groupdict() for exp in regexps if exp.match(shorthand)
        )

    # Handle short form of the type expression
    if "type" in attrs:
        attrs["type"] = INV_TYPECODE_MAP.get(attrs["type"], attrs["type"])

    return attrs


def infer_encoding_types(args, kwargs, channels):
    """Infer typed keyword arguments for args and kwargs
    Parameters
    ----------
    args : tuple
        List of function args
    kwargs : dict
        Dict of function kwargs
    channels : module
        The module containing all altair encoding channel classes.
    Returns
    -------
    kwargs : dict
        All args and kwargs in a single dict, with keys and types
        based on the channels mapping.
    """
    # Construct a dictionary of channel type to encoding name
    # TODO: cache this somehow?
    channel_objs = (getattr(channels, name) for name in dir(channels))
    channel_objs = (
        c for c in channel_objs if isinstance(c, type) and issubclass(c, SchemaBase)
    )
    channel_to_name = {c: c._encoding_name for c in channel_objs}
    name_to_channel = {}
    for chan, name in channel_to_name.items():
        chans = name_to_channel.setdefault(name, {})
        key = "value" if chan.__name__.endswith("Value") else "field"
        chans[key] = chan

    # First use the mapping to convert args to kwargs based on their types.
    for arg in args:
        if isinstance(arg, (list, tuple)) and len(arg) > 0:
            type_ = type(arg[0])
        else:
            type_ = type(arg)

        encoding = channel_to_name.get(type_, None)
        if encoding is None:
            raise NotImplementedError("positional of type {}" "".format(type_))
        if encoding in kwargs:
            raise ValueError("encoding {} specified twice.".format(encoding))
        kwargs[encoding] = arg

    def _wrap_in_channel_class(obj, encoding):
        if isinstance(obj, SchemaBase):
            return obj

        if isinstance(obj, str):
            obj = {"shorthand": obj}

        if isinstance(obj, (list, tuple)):
            return [_wrap_in_channel_class(subobj, encoding) for subobj in obj]

        # TODO: Separate encodings for each channel type?
        # if encoding not in name_to_channel:
        #     warnings.warn("Unrecognized encoding channel '{}'".format(encoding))
        #     return obj

        classes = name_to_channel[encoding]
        cls = classes["value"] if "value" in obj else classes["field"]

        try:
            # Don't force validation here; some objects won't be valid until
            # they're created in the context of a chart.
            return cls.from_dict(obj, validate=False)
        except jsonschema.ValidationError:
            # our attempts at finding the correct class have failed
            return obj

    return {
        encoding: _wrap_in_channel_class(obj, encoding)
        for encoding, obj in kwargs.items()
    }


def _compute_data_hash(data_str: str):
    return hashlib.md5(data_str.encode()).hexdigest()


def use_signature(Obj: Any):
    """Apply call signature and documentation of Obj to the decorated method"""

    def decorate(f):
        # call-signature of f is exposed via __wrapped__.
        # we want it to mimic Obj.__init__
        f.__wrapped__ = Obj.__init__
        f._uses_signature = Obj

        # Supplement the docstring of f with information from Obj
        if Obj.__doc__:
            doclines: List[str] = Obj.__doc__.splitlines()
            if f.__doc__:
                doc = f.__doc__ + "\n".join(doclines[1:])
            else:
                doc = "\n".join(doclines)
            try:
                f.__doc__ = doc
            except AttributeError:
                # __doc__ is not modifiable for classes in Python < 3.3
                pass

        return f

    return decorate
