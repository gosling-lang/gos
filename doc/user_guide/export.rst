.. currentmodule:: gosling

.. _export:

Exporting Visualization
=======================

A gosling visualization can be exported to either a **standalone HTML file** or a **JSON object** 
by calling the `save` function. The format of the exported visualization is determined by a file
extension you specify (i.e., `*.html` or `*.json`).

HTML
----

You can save an HTML file that embeds your Gosling visualization.

.. code-block:: python

    vis = gos.Track(
        gos.bigwig("https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig")
    ).encode(
        x='position:G',
        y='value:Q'
    ).view()

    vis.save('gosling.html')

The saved HTML file includes all resources that are needed to display Gosling visualization
for the web. When you open a saved HTML file on your browser, you will be able to see your 
visualization displayed on the page.

JSON
----

You can save the JSON object of your Gosling visualization. This object is a full specification 
of your Gosling visualization. You can copy and paste the object on the `Gosling Editor`_ to see
your visualization.

.. code-block:: python

    vis = gos.Track(
        gos.bigwig("https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig")
    ).encode(
        x='position:G',
        y='value:Q'
    ).view()

    vis.save('gosling.json')

.. code-block:: json

    {
        "tracks": [
            {
                "data": {
                    "type": "bigwig",
                    "url": "https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig"
                },
                "height": 180,
                "mark": "bar",
                "width": 800,
                "x": {
                    "field": "position",
                    "type": "genomic"
                },
                "y": {
                    "field": "value",
                    "type": "quantitative"
                }
            }
        ]
    }

.. _Gosling Editor: https://gosling.js.org/