.. currentmodule:: gosling

.. _local_data:

Motivation & Installation
=========================

`Data sources`_ for the Gosling_ specification are expected to be accessible via HTTP.
Loading a local dataset can be challenging since it requires starting a web-server
and/or a `Higlass server`_ for some pre-aggregated datasets. 

**gos** provides an experimental module that transparently serves data via a 
background ASGI server. The various data utilites are imported from 
the `gosling.experimental.data` module.

.. code-block:: python

    import gosling as gos
    from gosling.experimental.data import bam, csv, bigwig # file resources
    from gosling.experimental.data import beddb, vector, matrix, multivec # higlass tile resources


In order to use these utilities, you will need to install additional dependencies via:

.. code-block:: bash

    pip install 'gosling[all]' # installs extra deps for background data-server
    pip install clodius # optional, required for higlass tile resources


Usage
=====

The **gos** example below incudes a `multivec data source`_; the url points to a 
`Higlass server`_ endpoint for the corresponding tileset information. 

.. gosling-plot::
    :code-below:

    import gosling as gos
    from gosling.data import multivec

    data = multivec(
        url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
        row="sample",
        column="position",
        value="peak",
        categories=["sample 1", "sample 2", "sample 3", "sample 4"],
        binSize=5,
    )

    track = gos.Track(data).mark_rect().encode(
        x=gos.Channel("start:G", axis="top"),
        xe="end:G",
        row=gos.Channel("sample:N", legend=True),
        color=gos.Channel("peak:Q", legend=True),
    ).properties(width=725, height=100)

    track.view()


In the example above, we can replace the remote Higlass server URL with a local path to the
corresponding `cistrome multivec file`_ (4GB). **gos** automatically detects the local
file and will starts a background Higlass server to power the visualization.


.. code-block:: diff

    import gosling as gos
    -from gosling.data import multivec
    +from gosling.experimental.data import multivec

    data = multivec(
    -   url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
    +   url='../data/cistrome.multires.mv5', # path to local multivec
        row="sample",
        column="position",
        value="peak",
        categories=["sample 1", "sample 2", "sample 3", "sample 4"],
        binSize=4,
    )


Note that the visualizations will only render as long as your Python session is active.

.. _Data sources: https://gosling-lang.github.io/gosling-website/docs/data
.. _Higlass server: https://gosling-lang.github.io/gosling-website/docs/data#pre-aggregated-datasets-higlass-server
.. _multivec data source: http://gosling-lang.org/docs/data/#multivec
.. _Gosling: http://gosling-lang.org/
.. _cistrome multivec file: https://s3.amazonaws.com/gosling-lang.org/data/cistrome.multires.mv5
