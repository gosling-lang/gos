# gos 🦆

[![License](https://img.shields.io/pypi/l/gosling.svg?color=green)](https://github.com/gosling-lang/gos/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/gosling.svg?color=green)](https://pypi.org/project/gosling)
[![Python Version](https://img.shields.io/pypi/pyversions/gosling.svg?color=green)](https://python.org)
[![tests](https://github.com/gosling-lang/gos/workflows/Test/badge.svg)](https://github.com/gosling-lang/gos/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gosling-lang/gos/main?filepath=notebooks%2Fmultiple-coordinated-views.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gosling-lang/gos/blob/main/notebooks/multiple-coordinated-views.ipynb)

**gos** is a declarative (epi)genomics visualization library for Python.
It is built on top of the [Gosling] JSON specification, providing a
simplified interface for authoring interactive genomic visualizations.



## Installation

> The **gos** API is under active development. Feedback is appreciated and welcomed.

```bash
pip install gosling
```

## Documentation

See the [Documentation Site](https://gosling-lang.github.io/gos) for more information.

## Example

<img src="https://github.com/gosling-lang/gos/raw/main/doc/_static/example.gif" alt="Gosling visualization" width="800" />

```python
import gosling as gos

data = gos.multivec(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1", "sample 2", "sample 3", "sample 4"],
    binSize=5,
)

base_track = gos.Track(data, width=800, height=100)

heatmap = base_track.mark_rect().encode(
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    row=gos.Row("sample:N", legend=True),
    color=gos.Color("peak:Q", legend=True),
)

bars = base_track.mark_bar().encode(
    x=gos.X("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Color("sample:N", legend=True),
)

lines = base_track.mark_line().encode(
    x=gos.X("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Color("sample:N", legend=True),
)

gos.vertical(heatmap, bars, lines).properties(
    title="Visual Encoding",
    subtitle="Gosling provides diverse visual encoding methods",
    layout="linear",
    centerRadius=0.8,
    xDomain=gos.GenomicDomain(chromosome="1", interval=[1, 3000500]),
)
```

## Example Gallery

We have started a [gallery](https://gosling-lang.github.io/gos/gallery/index.html) of
community examples in `gosling/examples/`. If you are interested in contributing, please
feel free to submit a PR! Checkout the [existing JSON examples](http://gosling-lang.org/examples/)
if you are looking for inspiration.


## Development

```bash
pip install -e '.[dev]'
```

The schema bindings (`gosling/schema/`) and docs (`doc/user_guide/API.rst`) are 
automatically generated using the following. Please do not edit these
files directly.

```bash
# generate gosling/schema/*
python tools/generate_schema_wrapper.py
```

## Release

```bash
git checkout main && git pull
```

Update version in `setup.py` and `doc/conf.py`:

```bash
git add setup.py doc/conf.py
git commit -m "v0.[minor].[patch]"
git tag -a v0.[minor].[patch] -m "v0.[minor].[patch]"
git push --follow-tags
```

## Design & Implementation

gos is inspired by and borrows heavily from [Altair] both in project philosophy
and implementation. The internal Python API is auto-generated from the
[Gosling] specification using code adapted directly from Altair to generate
[Vega-Lite] bindings. This design choice guarantees that visualizations are
type-checked in complete concordance with the [Gosling] specification, and that
the Python API remains consistent with the evolving schema over time. Special thanks to
[Jake Vanderplas](https://github.com/jakevdp) and others on
[`schemapi`](https://github.com/altair-viz/altair/tree/master/tools/schemapi).

[Gosling]: https://github.com/gosling-lang/gosling.js
[Altair]: https://github.com/altair-viz/altair
[Vega-Lite]: https://github.com/vega/vega-lite
