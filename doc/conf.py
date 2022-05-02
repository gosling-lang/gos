# !/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "numpydoc.numpydoc",
    "gosling.sphinxext.gallery",
    "gosling.sphinxext.plot",
]

autodoc_default_flags = ["members", "inherited-members"]

autodoc_member_order = "groupwise"

autosummary_generate = True

numpydoc_show_class_members = False

templates_path = ["_templates"]

source_suffix = ".rst" # ['.rst', '.md']

master_doc = "index"

project = "gos"
copyright = "2021, Trevor Manz"
author = "Trevor Manz"

version = "0.0.8"
release = version

todo_include_todos = False

html_theme = 'furo'

html_title = "gos"
html_short_title = "gos"

# The name of an image file (relative to this directory) to place at the top of the sidebar.
html_logo = "_static/favicon.png"

html_favicon = "_static/favicon.ico"

html_static_path = ["_static"]

html_css_files = ["theme_overrides.css"]

