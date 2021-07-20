import sys
import os
import json
import pathlib
from urllib import request
from typing import Optional, TypeVar

# import schemapi from here
sys.path.insert(0, pathlib.Path.cwd())
from schemapi import codegen
from schemapi.codegen import CodeSnippet
from schemapi.utils import (
    get_valid_identifier,
    SchemaInfo,
    indent_arglist,
    resolve_references,
)

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

# Map of version name to github branch name.
SCHEMA_VERSION = {
    "gosling": {"v0": ""},
}

SCHEMA_URL_TEMPLATE = "https://raw.githubusercontent.com/gosling-lang/gosling.js/master/schema/gosling.schema.json"


def schema_class(*args, **kwargs):
    return codegen.SchemaGenerator(*args, **kwargs).schema_class()


def schema_url(library: str, version: str):
    version = SCHEMA_VERSION[library][version]
    return SCHEMA_URL_TEMPLATE.format(library=library, version=version)


def download_schemafile(
    library: str,
    version: str,
    schemapath: pathlib.Path,
    skip_download: Optional[bool] = False,
) -> pathlib.Path:
    url = schema_url(library, version)
    if not schemapath.exists():
        os.makedirs(schemapath)
    filename = schemapath / "{library}-schema.json".format(library=library)
    if not skip_download:
        request.urlretrieve(url, filename)
    elif not filename.exists():
        raise ValueError(f"Cannot skip download: {filename} does not exist")
    return filename


def toposort(graph: dict[list[T]]) -> list[T]:
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
    Copy the schemapi utility and its test file into altair/utils/
    """
    current_dir = pathlib.Path(__file__).parent

    # copy the schemapi utility file
    source_path = current_dir / "schemapi" / "schemapi.py"
    destination_path = current_dir / ".." / "gosling" / "utils" / "schemapi.py"

    if not destination_path.exists():
        os.makedirs(destination_path.parent)

    print(f"Copying\n {source_path}\n  -> {destination_path}")
    with open(source_path, "r", encoding="utf8") as source:
        with open(destination_path, "w", encoding="utf8") as dest:
            dest.write(HEADER)
            dest.writelines(source.readlines())

    # Copy the schemapi test file
    source_path = current_dir / "schemapi" / "tests" / "test_schemapi.py"
    destination_path = (
        current_dir / ".." / "gosling" / "utils" / "tests" / "test_schemapi.py"
    )

    if not destination_path.exists():
        os.makedirs(destination_path.parent)

    print(f"Copying\n {source_path}\n  -> {destination_path}")
    with open(source_path, "r", encoding="utf8") as source:
        with open(destination_path, "w", encoding="utf8") as dest:
            dest.write(HEADER)
            dest.writelines(source.readlines())


def generate_gosling_schema_wrapper(schema_file: pathlib.Path):
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
        "from gosling.utils.schemapi import SchemaBase, Undefined, _subclasses",
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


def gosling_main(skip_download: Optional[bool] = False):
    library = "gosling"

    for version in SCHEMA_VERSION[library]:
        schemapath = pathlib.Path(__file__).parent / ".." / "gosling" / "schema"
        schemafile = download_schemafile(
            library=library,
            version=version,
            schemapath=schemapath,
            skip_download=skip_download,
        )

        # Generate __init__.py file
        outfile = schemapath / "__init__.py"
        print(f"Writing {outfile}")
        with open(outfile, "w", encoding="utf8") as f:
            f.write("# flake8: noqa\n")
            f.write("from .core import *\n")
            f.write(f"SCHEMA_VERSION = {SCHEMA_VERSION[library][version]!r}\n")
            f.write(f"SCHEMA_URL = {schema_url(library, version)!r}\n")

        # Generate the core schema wrappers
        outfile = schemapath / "core.py"
        print(f"Generating\n {schemafile}\n  ->{outfile}")
        file_contents = generate_gosling_schema_wrapper(schemafile)
        with open(outfile, "w", encoding="utf8") as f:
            f.write(file_contents)


if __name__ == "__main__":
    copy_schemapi_util()
    gosling_main()
