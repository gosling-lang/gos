# ipygosling


## Example

```python
import gosling as gos

multivec = gos.Data(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
    type="multivec",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1", "sample 2", "sample 3", "sample 4"],
    binSize=5,
)

base_track = gos.Track(data=multivec, width=800, height=100)

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

gos.vertical(heatmap.view(), bars.view(), lines.view()).properties(
    title="Visual Encoding",
    subtitle="Gosling provides diverse visual encoding methods",
    layout="linear",
    centerRadius=0.8,
    xDomain=gos.Domain(chromosome="1", interval=[1, 3000500]),
)
```

<img src="https://github.com/manzt/ipygosling/raw/enhance-readme/images/example.gif" alt="Gosling visualization" width="800" />


## Installation

**Here be dragons 🐉**

> The API is *experimental* and under active development.
> Feedback is much appreciated and most welcomed.

```bash
pip install gosling
```


## Add an example

We have started a gallery of community examples in `example/`. If you are 
intereseted in contributing, please feel free to submit a PR! Checkout the
[existing JSON examples](http://gosling-lang.org/examples/) if you are
looking for inspiration.

## Development

```bash
pip install -e .
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

