"""
This script fills the contents of doc/user_guide/API.rst
based on the updated Altair schema.
"""
from os.path import abspath, dirname, join
import sys
import types

# Import Altair from head
ROOT_DIR = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import gosling as gos
import gosling.api as api

API_FILENAME = join(ROOT_DIR, "doc", "user_guide", "API.rst")

API_TEMPLATE = """\
.. _API:
API Reference
=============
This is the class and function reference of **gos**, and the following content
is generated automatically from the code documentation strings.
This low-level documentation may not be enough to give full guidelines on their use.

Top-Level Objects
-----------------
.. currentmodule:: gosling
.. autosummary::
   :toctree: generated/toplevel/
   :nosignatures:

   View
   Track
Encoding Channels
-----------------
.. currentmodule:: gosling
.. autosummary::
   :toctree: generated/channels/
   :nosignatures:

   {encoding_wrappers}
API Functions
-------------
.. currentmodule:: gosling
.. autosummary::
   :toctree: generated/api/
   :nosignatures:

   {api_functions}
Low-Level Schema Wrappers
-------------------------
.. currentmodule:: gosling
.. autosummary::
   :toctree: generated/core/
   :nosignatures:

   {lowlevel_wrappers}
"""


def iter_objects(
    mod, ignore_private=True, restrict_to_type=None, restrict_to_subclass=None
):
    for name in dir(mod):
        obj = getattr(mod, name)
        if ignore_private:
            if name.startswith("_"):
                continue
        if restrict_to_type is not None:
            if not isinstance(obj, restrict_to_type):
                continue
        if restrict_to_subclass is not None:
            if not (isinstance(obj, type) and issubclass(obj, restrict_to_subclass)):
                continue
        yield name

def encoding_wrappers():
    return sorted(iter_objects(gos.channels, restrict_to_subclass=gos.SchemaBase))

def api_functions():
    return sorted(iter_objects(api, restrict_to_type=types.FunctionType))

def lowlevel_wrappers():
    return sorted(iter_objects(gos.core, restrict_to_subclass=gos.SchemaBase))


def write_api_file():
    print("Updating API docs\n  ->{}".format(API_FILENAME))
    sep = "\n   "
    with open(API_FILENAME, "w") as f:
        f.write(
            API_TEMPLATE.format(
                api_functions=sep.join(api_functions()),
                encoding_wrappers=sep.join(encoding_wrappers()),
                lowlevel_wrappers=sep.join(lowlevel_wrappers()),
            )
        )


if __name__ == "__main__":
    write_api_file()

