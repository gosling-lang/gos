# gos 🦆

[![License](https://img.shields.io/pypi/l/gosling.svg?color=green)](https://github.com/gosling-lang/gos/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/gosling.svg?color=green)](https://pypi.org/project/gosling)
[![Python Version](https://img.shields.io/pypi/pyversions/gosling.svg?color=green)](https://python.org)
[![tests](https://github.com/gosling-lang/gos/workflows/Test/badge.svg)](https://github.com/gosling-lang/gos/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gosling-lang/gos/main?filepath=notebooks%2Fmultiple-coordinated-views.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gosling-lang/gos/blob/main/notebooks/multiple-coordinated-views.ipynb)

**gos** is a declarative (epi)genomics visualization library for Python.
It is built on top of the [Gosling] JSON specification, providing an
simplified interface for authoring interactive genomic visualizations.



## Installation

**Here be dragons 🐉**

> The API is under active development. Feedback is much appreciated and most welcomed.

```bash
pip install gosling
```

## Documentation

See the [Documentation Site](https://gosling-lang.github.io/gos) for more information.

## Example

```python
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

base_track = gos.Track(data, width=800, height=100)

heatmap = base_track.mark_rect().encode(
    x=gos.Channel("start:G", axis="top"),
    xe="end:G",
    row=gos.Channel("sample:N", legend=True),
    color=gos.Channel("peak:Q", legend=True),
)

bars = base_track.mark_bar().encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Channel("sample:N", legend=True),
)

lines = base_track.mark_line().encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Channel("sample:N", legend=True),
)

gos.vertical(heatmap, bars, lines).properties(
    title="Visual Encoding",
    subtitle="Gosling provides diverse visual encoding methods",
    layout="linear",
    centerRadius=0.8,
    xDomain=gos.Domain(chromosome="1", interval=[1, 3000500]),
)
```

<img src="https://github.com/gosling-lang/gos/raw/main/doc/_static/example.gif" alt="Gosling visualization" width="800" />


## Example Gallery

We have started a gallery of community examples in `gosling/examples/`. If you are 
intereseted in contributing, please feel free to submit a PR! Checkout the
[existing JSON examples](http://gosling-lang.org/examples/) if you are
looking for inspiration.


## Development

```bash
pip install -e '.[dev]'
```

The schema bindings (`gosling/schema/`) and JS static assets (`gosling/static/`)
are automatically generated using the following scripts. Please do not edit these
files directly.

```bash
# generate gosling/schema/*
python tools/generate_schema_wrapper.py

# generate gosling/static/{widget.js,index.js} from src/{widget.ts,index.ts}
yarn install && yarn build:js

# Only run this if editing/using gos.GoslingWidget
jupyter nbextension install --py --symlink --overwrite --sys-prefix gosling
jupyter nbextension enable gosling --py --sys-prefix
```


## Design & implemenation

gos is inspired by and borrows heavily from [Altair] both in project philosophy
and implementation. The internal Python API is auto-generated from the
[Gosling] specification using code adapted directly from Altair to generate
[Vega-Lite] bindings. This design choice gaurentees that visualizations are
type-checked in complete concordance with the [Gosling] specification, and that
the Python API remains consitent with the evolving schema over time. Special thanks to
[Jake Vanderplas](https://github.com/jakevdp) and others on
[`schemapi`](https://github.com/altair-viz/altair/tree/master/tools/schemapi).

[Gosling]: https://github.com/gosling-lang/gosling.js
[Altair]: https://github.com/altair-viz/altair
[Vega-Lite]: https://github.com/vega/vega-lite
