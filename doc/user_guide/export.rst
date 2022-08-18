.. currentmodule:: gosling

.. _export:

Exporting Gosling Visualization
===============================

A Gosling visualization created using **gos** can be exported to either a standalone 
HTML file or a JSON value.

HTML
----

You can save an HTML file that embeds your Gosling visualization.

.. code-block:: python

    vis = gos.Track(...).encode(...).view()
    vis.save('index.html')

When you open a saved HTML file on your browser, you will be able to see your 
visualization displayed on the page.

JSON
----

You can save the JSON object of your Gosling visualization. This object contains 
all the information needed to draw your visualization. For example, you can copy and 
paste the object on the `Gosling Editor` to see your visualization.

.. code-block:: python

    vis = gos.Track(...).encode(...).view()
    vis.to_json()

.. _Gosling Editor: https://gosling.js.org/