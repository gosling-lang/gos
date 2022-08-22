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
on the webpage.

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <style>.error { color: red; }</style>
        <link rel="stylesheet" href="https://esm.sh/higlass@1.11/dist/hglib.css">
    </head>
    <body>
        <div id="vis"></div>
        <script type="module">
            import * as gosling from "https://esm.sh/gosling.js@0.9.22?bundle&deps=react-dom@17,react@17,pixi.js@6,higlass@1.11";
            let el = document.querySelector('#vis');
            let spec = {"tracks": [{"data": {"type": "bigwig", "url": "https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig"}, "mark": "bar", "height": 180, "width": 800, "x": {"field": "position", "type": "genomic"}, "y": {"field": "value", "type": "quantitative"}}]};
            let opts = {"padding": 0, "theme": null};
            gosling.embed(el, spec, opts).catch(err => {
                el.innerHTML = `<div class="error">
                        <p>JavaScript Error: ${error.message}</p>
                        <p>This usually means there's a typo in your Gosling specification. See the javascript console for the full traceback.</p>
                    </div>`;
                throw error;
            });
        </script>
    </body>
    </html>

If you open the HTML file on your browser, you will be able to see your 
visualization displayed on the page.

JSON
----

You can save the JSON object of your Gosling visualization.

.. code-block:: python

    vis = gos.Track(
        gos.bigwig("https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig")
    ).encode(
        x='position:G',
        y='value:Q'
    ).view()

    vis.save('gosling.json')

This object is a full specification of your Gosling visualization. You can copy the object and 
paste it on the `Gosling Editor`_ to display your visualization.

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