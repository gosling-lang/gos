# gos 🦆

[![License](https://img.shields.io/pypi/l/gosling.svg?color=green)](https://github.com/gosling-lang/gos/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/gosling.svg?color=green)](https://pypi.org/project/gosling)
[![tests](https://github.com/gosling-lang/gos/workflows/CI/badge.svg)](https://github.com/gosling-lang/gos/actions)

**gos** is a declarative genomics visualization library for Python. It is built
on top of the [Gosling] JSON specification, providing a simplified interface for
authoring interactive genomic visualizations.

## Installation

> The **gos** API is under active development. Feedback is appreciated and
> welcomed.

```bash
pip install gosling[all]
```

## Documentation

See the [Documentation Site](https://gosling-lang.github.io/gos) for more
information.

## Example

<img src="https://raw.githubusercontent.com/gosling-lang/gos/main/docs/_static/example.gif" alt="Gosling visualization"/>

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

We have started a
[gallery](https://gosling-lang.github.io/gos/gallery/index.html) of community
examples in `gosling/examples/`. If you are interested in contributing, please
feel free to submit a PR! Checkout the
[existing JSON examples](http://gosling-lang.org/examples/) if you are looking
for inspiration.

## Changelog

Check the [GitHub Releases](https://github.com/gosling-lang/gos/releases) for a
detailed changelog.

## **Development**

The source code for **gos** is a hybrid of Python and TypeScript (used for the
[anywidget](https://github.com/manzt/anywidget) component). It requires both:

- [uv](https://github.com/astral-sh/uv) (for Python development)
- [Deno](https://deno.land) (for building the widget)

Please ensure both are installed before proceeding.

**Tests**

Run the test suite with:

```sh
uv run pytest
```

**Notebooks**

To try out the library in the example `notebooks/`, launch Jupyter Lab with:

```sh
uv run jupyter lab
```

**Widget**

The widgets implementation is split between `./gosling/_widget.py` (the Python
component) and `./frontend/widget.ts` (the TypeScript component).

To modify the widget's behavior in the front end, edit `./frontend/widget.ts`
and compile with:

```sh
deno task build
```

Use `deno task dev` to watch for changes and recompile automatically.

**Docs**

To build and preview the documentation locally:

```sh
uv run docs/build.py
uv run python -m http.server -d docs/dist
```

Open your browser to http://localhost:8000 to view the generated docs.

**Auto-generate Schema Bindings**

Much of the Python code in this repository is automatically generated from the
Gosling schema to keep the bindings in sync. This includes both the bindings in
`gosling/schema/` and the corresponding API documentation in
`doc/user_guide/API.rst`.

Do not edit these files manually. Instead, regenerate them using:

```sh
# Update gosling/schema/*
uv run tools/generate_schema_wrapper.py <tag_name>
# Update API docs
uv run tools/generate_api_docs.py
```

Use a `tag_name` that corresponds to a valid
[Gosling.js Release](https://github.com/gosling-lang/gosling.js/releases) (e.g.,
`v0.12.3`).

You must commit the changes and create a new release. Schema updates usually
require at least a minor version bump, but the exact versioning is up to the
maintainer.

## Release

Releases are managed via the GitHub UI. The release **tag determines the package
version** published to PyPI.

[Draft a new release](https://github.com/gosling-lang/gos/releases/new):

1. **Create a tag**

   - Click _"Choose a tag"_, then **type a new tag** in the format
     `v[major].[minor].[patch]` to create it.
   - _Note_: The UI is not obvious about this. You can create a tag here, not
     just select one.

2. **Generate release notes**

   - Click _"Generate Release Notes"_ to auto-summarize changes from merged PRs.
   - Edit to exclude irrelevant changes for end users (e.g., docs or CI).

3. **Document significant changes**

   - Add migration steps or noteworthy updates.
   - Ensure PR titles are clear and consistent.

4. **Publish the release**

   - Click _Publish release_ to make it public.
   - This triggers a [workflow](.github/workflows/release.yml) that builds the
     package and publishes it to PyPI using the new tag.

## Design & Implementation

gos is inspired by and borrows heavily from [Altair] both in project philosophy
and implementation. The internal Python API is auto-generated from the [Gosling]
specification using code adapted directly from Altair to generate [Vega-Lite]
bindings. This design choice guarantees that visualizations are type-checked in
complete concordance with the [Gosling] specification, and that the Python API
remains consistent with the evolving schema over time. Special thanks to
[Jake Vanderplas](https://github.com/jakevdp) and others on
[`schemapi`](https://github.com/altair-viz/altair/tree/master/tools/schemapi).

[Gosling]: https://github.com/gosling-lang/gosling.js
[Altair]: https://github.com/altair-viz/altair
[Vega-Lite]: https://github.com/vega/vega-lite
