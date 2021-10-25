.. currentmodule:: gosling

.. _themes:

Themes
======

Themes customize the look of Gosling visualizations. To enable themes with **gos**, use
the :code:`gos.themes` namespace:

.. code-block:: python

    import gosling as gos
    gos.themes.enable("dark") # sets theme globally

    gos.Track(...).encode(...).view()


You can explore supported themes in the `Theme Playground`_.

.. _Theme Playground: http://gosling-lang.org/themes/
