.. currentmodule:: gosling

.. _installation:

Installation
============
**gos** can be installed using::

    $ pip install gosling


Dependencies
============

**gos** has the following dependencies, all of which are installed automatically
with the above installation commands:

- python 3.7 or newer
- jsonschema_
- NumPy_
- Pandas_

To run the full test suite and build documentation requires a few additional dependencies:

- pytest
- jinja2
- sphinx
- m2r
- ipython

Development Install
===================

The `gos source repository`_ is available on GitHub. Once you have cloned the
repository and installed all the above dependencies, run the following command
from the root of the repository to install the main version of **gos**:

.. code-block:: bash

    $ pip install -e .

To install development dependencies as well, run

.. code-block:: bash

    $ pip install -e .[dev]

.. _JupyterLab: http://jupyterlab.readthedocs.io/
.. _Jupyter Notebook: https://jupyter-notebook.readthedocs.io/

.. _jsonschema: https://github.com/Julian/jsonschema
.. _NumPy: http://www.numpy.org/
.. _Pandas: http://pandas.pydata.org
.. _gos source repository: http://github.com/manzt/gos
