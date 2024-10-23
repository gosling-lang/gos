.. currentmodule:: gosling

.. _themes:

Themes
======

To enable themes with **gos**, use the :code:`gos.themes` registry:

.. code-block:: python

    import gosling as gos
    gos.themes.enable("dark") # sets theme globally

    gos.Track(...).encode(...).view()


You can explore the available built-in themes in the `Theme Playground`_.


Custom Themes
=============

A custom theme may be specified by extending an existing built-in theme, or creating a 
theme from scratch, and adding it to the :code:`gos.themes` registry.

.. code-block:: python

    import gosling as gosling

    my_theme = { "base": "dark", "axis": { "baselineColor": "green" } }
    gos.themes.register("my-theme", my_theme) # add theme to registry
    gos.themes.enable("my-theme") # enable custom theme



.. _Theme Playground: http://gosling-lang.org/themes/
