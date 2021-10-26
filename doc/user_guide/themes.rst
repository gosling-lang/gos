.. currentmodule:: gosling

.. _themes:

Themes
======

Themes modify the look of Gosling visualizations. To enable themes with **gos**, use
the :code:`gos.themes` namespace:

.. code-block:: python

    import gosling as gos
    gos.themes.enable("dark") # sets theme globally

    gos.Track(...).encode(...).view()


You can explore built-in themes in the `Theme Playground`_.


Custom Themes
=============

A custom theme may be specified by modifying by existing built-in theme, or creating a 
theme from scratch, and registering it globally.

.. code-block:: python

    import gosling as gosling

    my_theme = { "base": "dark", "axis": { "baselineColor": "green" }
    gos.themes.register("my-theme", my_theme) # add theme to registry
    gos.themes.enable("my-theme") # enable custom theme



.. _Theme Playground: http://gosling-lang.org/themes/
