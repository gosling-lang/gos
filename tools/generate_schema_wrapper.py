import sys
import copy
import os
import json
import pathlib
from urllib import request
import textwrap
from typing import Optional, TypeVar

# import schemapi from here
here = pathlib.Path(__file__)
sys.path.insert(0, str(here.parent))

from schemapi import codegen
from schemapi.codegen import CodeSnippet
from schemapi.utils import (
    get_valid_identifier,
    SchemaInfo,
    indent_arglist,
    resolve_references,
)
import generate_api_docs  # noqa: E402

T = TypeVar("T")

HEADER = """\
# The contents of this file are automatically written by
# tools/generate_schema_wrapper.py. Do not modify directly.
"""

BASE_SCHEMA = """
class {basename}(SchemaBase):
    _rootschema = load_schema()
    @classmethod
    def _default_wrapper_classes(cls):
        return _subclasses({basename})
"""

LOAD_SCHEMA = '''
import pkgutil
import json

def load_schema():
    """Load the json schema associated with this module's functions"""
    return json.loads(pkgutil.get_data(__name__, '{schemafile}').decode('utf-8'))
'''

CHANNEL_MIXINS = """
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
"""


class FieldSchemaGenerator(codegen.SchemaGenerator):
    schema_class_template = textwrap.dedent(
        '''
    class {classname}(FieldChannelMixin, core.{basename}):
        """{docstring}"""
        _class_is_valid_at_instantiation = False
        _encoding_name = "{encodingname}"

        {init_code}
    '''
    )


class ValueSchemaGenerator(codegen.SchemaGenerator):
    schema_class_template = textwrap.dedent(
        '''
    class {classname}(ValueChannelMixin, core.{basename}):
        """{docstring}"""
        _class_is_valid_at_instantiation = False
        _encoding_name = "{encodingname}"

        {init_code}
    '''
    )


GOSLING_URL_TEMPLATE = "https://raw.githubusercontent.com/gosling-lang/{library}/{version}/schema/{filename}"

def schema_class(*args, **kwargs):
    return codegen.SchemaGenerator(*args, **kwargs).schema_class()


def schema_url(library: str, version: str):
    return GOSLING_URL_TEMPLATE.format(
        library=library, version=version, filename="gosling.schema.json"
    )


def theme_url(library: str, version: str):
    return GOSLING_URL_TEMPLATE.format(
        library=library, version=version, filename="theme.schema.json"
    )


def download_schemafile(
    library: str,
    version: str,
    schemapath: pathlib.Path,
    skip_download: Optional[bool] = False,
) -> pathlib.Path:
    url = schema_url(library, version)
    if not schemapath.exists():
        os.makedirs(schemapath)
    filename = schemapath / f"{library.rstrip('.js')}-schema.json"
    if not skip_download:
        request.urlretrieve(url, filename)
    elif not filename.exists():
        raise ValueError(f"Cannot skip download: {filename} does not exist")
    return filename


def toposort(graph: dict[str, list[T]]) -> list[T]:
    """Topological sort of a directed acyclic graph.

    Parameters
    ----------
    graph : dict of lists
        Mapping of node labels to list of child node labels.
        This is assumed to represent a graph with no cycles.

    Returns
    -------
    order : list
        topological order of input graph.
    """
    stack = []
    visited = set()

    def visit(nodes):
        for node in sorted(nodes, reverse=True):
            if node not in visited:
                visited.add(node)
                visit(graph.get(node, []))
                stack.insert(0, node)

    visit(graph)
    return stack


def copy_schemapi_util():
    """
    Copy the schemapi utility and its test file into gosling/utils/
    """
    current_dir = here.parent
    # copy the schemapi utility file
    source_path = current_dir / "schemapi" / "schemapi.py"
    destination_path = current_dir / ".." / "gosling" / "schemapi.py"

    if not destination_path.parent.exists():
        os.makedirs(destination_path.parent)

    print(f"Copying\n {source_path}\n  -> {destination_path}")
    with open(source_path, "r", encoding="utf8") as source:
        with open(destination_path, "w", encoding="utf8") as dest:
            dest.write(HEADER)
            dest.writelines(source.readlines())


def generate_schema_wrapper(schema_file: pathlib.Path):
    """Generate a schema wrapper at the given path."""
    # TODO: generate simple tests for each wrapper
    basename = "GoslingSchema"

    with open(schema_file, encoding="utf8") as f:
        rootschema = json.load(f)

    definitions = {}

    for name in rootschema["definitions"]:
        defschema = {"$ref": f"#/definitions/{name}"}
        defschema_repr = {"$ref": f"#/definitions/{name}"}
        name = get_valid_identifier(name)
        definitions[name] = codegen.SchemaGenerator(
            name,
            schema=defschema,
            schemarepr=defschema_repr,
            rootschema=rootschema,
            basename=basename,
            rootschemarepr=CodeSnippet(f"{basename}._rootschema"),
        )

    graph = {}

    for name, schema in definitions.items():
        graph[name] = []
        for child in schema.subclasses():
            child = get_valid_identifier(child)
            graph[name].append(child)
            child = definitions[child]
            if child.basename == basename:
                child.basename = [name]
            else:
                child.basename.append(name)

    contents = [
        HEADER,
        "from gosling.schemapi import SchemaBase, Undefined, _subclasses",
        LOAD_SCHEMA.format(schemafile="gosling-schema.json"),
    ]
    contents.append(BASE_SCHEMA.format(basename=basename))
    contents.append(
        schema_class(
            "Root",
            schema=rootschema,
            basename=basename,
            schemarepr=CodeSnippet(f"{basename}._rootschema"),
        )
    )

    for name in toposort(graph):
        contents.append(definitions[name].schema_class())

    contents.append("")  # end with newline
    return "\n".join(contents)


def generate_channel_wrappers(schemafile, imports=None):
    # TODO: generate __all__ for top of file
    with open(schemafile, encoding="utf8") as f:
        schema = json.load(f)
    if imports is None:
        imports = [
            "from . import core",
            # "import pandas as pd",
            "from gosling.schemapi import Undefined",
            "import gosling.utils as utils",
        ]
    contents = [HEADER]
    contents.extend(imports)
    contents.append("")

    contents.append(CHANNEL_MIXINS)

    encoding_def = "SingleTrack"
    encoding = SchemaInfo(schema["definitions"][encoding_def], rootschema=schema)

    # Iterate over all properties defined on `SingleTrack` since encoding fields
    # are defined at the same level as non-encoding fields. We filter for visual
    # channel properties since they are distinguished by `ChannelValue` option.
    # TODO: https://github.com/gosling-lang/gosling.js/pull/533#discussion_r726263624
    for prop, propschema in encoding.properties.items():
        if propschema.is_reference():
            # all our visual encodings are anyOf(<Type>, ChannelValue),
            # so a reference here is for a non encoding field
            # definitions = [propschema.ref]
            definitions = []
        elif propschema.is_anyOf():
            definitions = [s.ref for s in propschema.anyOf if s.is_reference()]
            if not any("ChannelValue" in d for d in definitions):
                definitions = []
        else:
            # raise ValueError("either $ref or anyOf expected")
            definitions = []

        for definition in definitions:
            defschema = {"$ref": definition}
            basename = definition.split("/")[-1]
            classname = prop[0].upper() + prop[1:]

            if "Value" in basename:
                Generator = ValueSchemaGenerator
                classname += "Value"
                nodefault = ["value"]
            else:
                Generator = FieldSchemaGenerator
                nodefault = []
                defschema = copy.deepcopy(resolve_references(defschema, schema))

                # For Encoding field definitions, we patch the schema by adding the
                # shorthand property.
                defschema["properties"]["shorthand"] = {
                    "type": "string",
                    "description": "shorthand for field, aggregate, and type",
                }
                defschema["required"] = ["shorthand"]

            gen = Generator(
                classname=classname,
                basename=basename,
                schema=defschema,
                rootschema=schema,
                encodingname=prop,
                nodefault=nodefault,
            )
            contents.append(gen.schema_class())
    return "\n".join(contents)


MARK_METHOD = '''
def mark_{mark}({def_arglist}) -> T:
    """Set the track's mark to '{mark}'

    For information on additional arguments, see :class:`{style_def}`
    """
    kwds = dict({dict_arglist})
    copy = self.copy()
    copy.mark = "{mark}"
    if any(val is not Undefined for val in kwds.values()):
        copy.style = core.{style_def}(**kwds)
    return copy
'''


def generate_mark_mixin(schemafile: pathlib.Path, mark_enum: str, style_def: str):
    with open(schemafile, encoding="utf8") as f:
        schema = json.load(f)

    imports = [
        "from typing import TypeVar",
        "from gosling.schemapi import Undefined",
        "from . import core",
    ]

    code = [
        "T = TypeVar('T')",
        "class MarkMethodMixin(object):",
        '    """A mixin class that defines mark methods"""',
    ]

    marks = schema["definitions"][mark_enum]["enum"]
    info = SchemaInfo({"$ref": "#/definitions/" + style_def}, rootschema=schema)

    # adapted from SchemaInfo.init_code
    _, required, kwds, invalid_kwds, additional = codegen._get_args(info)
    required -= {"type"}
    kwds -= {"type"}

    def_args = ["self: T"] + [
        "{}=Undefined".format(p) for p in (sorted(required) + sorted(kwds))
    ]
    dict_args = ["{0}={0}".format(p) for p in (sorted(required) + sorted(kwds))]

    if additional or invalid_kwds:
        def_args.append("**kwds")
        dict_args.append("**kwds")

    for mark in marks:
        # TODO: only include args relevant to given type?
        mark_method = MARK_METHOD.format(
            mark=mark,
            style_def=style_def,
            def_arglist=indent_arglist(def_args, indent_level=10 + len(mark)),
            dict_arglist=indent_arglist(dict_args, indent_level=16),
        )
        code.append("\n    ".join(mark_method.splitlines()))

    return imports, "\n".join(code)


def main(skip_download: Optional[bool] = False):
    library = "gosling.js"
    version = "v0.9.16"

    schemapath = here.parent / ".." / "gosling" / "schema"
    schemafile = download_schemafile(
        library=library,
        version=version,
        schemapath=schemapath,
        skip_download=skip_download,
    )

    # extract theme names
    # TODO(2021-11-01): Use same version as schema, not latest. Should be able to remove for >= v0.9.9
    with request.urlopen(theme_url(library, version="master")) as f:
        themes_schema = json.loads(f.read())
        themes = themes_schema["definitions"]["ThemeType"]["enum"]

    # Generate __init__.py file
    outfile = schemapath / "__init__.py"
    print(f"Writing {outfile}")
    with open(outfile, "w", encoding="utf8") as f:
        f.write("# flake8: noqa\n")
        f.write("from .core import *\n")
        f.write("from .channels import *\n")
        f.write(f"SCHEMA_VERSION = {repr(version)}\n")
        f.write(f"SCHEMA_URL = {repr(schema_url(library, version))}\n")
        # sort themes alphabetically, change from list to set
        f.write(f"THEMES = {sorted(themes)}\n".replace("[", "{").replace("]", "}"))

    # Generate the core schema wrappers
    outfile = schemapath / "core.py"
    print(f"Generating\n {schemafile}\n  ->{outfile}")
    file_contents = generate_schema_wrapper(schemafile)
    with open(outfile, "w", encoding="utf8") as f:
        f.write(file_contents)

    # Generate the channel wrappers
    outfile = schemapath / "channels.py"
    print("Generating\n {}\n  ->{}".format(schemafile, outfile))
    code = generate_channel_wrappers(schemafile)
    with open(outfile, "w", encoding="utf8") as f:
        f.write(code)

    # generate the mark mixin
    outfile = schemapath / "mixins.py"
    print("Generating\n {}\n  ->{}".format(schemafile, outfile))
    mark_imports, mark_mixin = generate_mark_mixin(
        schemafile,
        mark_enum="Mark",
        style_def="Style",
    )
    imports = sorted(set(mark_imports))
    with open(outfile, "w", encoding="utf8") as f:
        f.write(HEADER)
        f.write("\n".join(imports))
        f.write("\n\n\n")
        f.write(mark_mixin)


if __name__ == "__main__":
    copy_schemapi_util()
    main()
    generate_api_docs.write_api_file()
