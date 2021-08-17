# ipygosling

**Here be dragons 🐉**

> This is an *experimental* project that is planned to merge with 
> [`gosling.py`](https://github.com/gosling-lang/gosling.py). Feedback is 
> much appreciated and most welcomed. _Please use with caution_.

## Generate source code 

The schema bindings (`gosling/schema`) and JS static assets (`gosling/static/`)
are automatically generated using the following scripts. Please do not edit these
files directly.

#### Python schema bindings

```bash
python tools/generate_schema_wrapper.py # generates gosling/schema/*
pip install -e .
```

#### JavScript Jupyter extension/widget

```bash
yarn install && yarn build # generates gosling/static/{widget.js, index.js}

jupyter nbextension install --py --symlink --overwrite --sys-prefix gosling
jupyter nbextension enable gosling --py --sys-prefix
```

## Usage

```python
import gosling as gos

data = gos.Data(
    url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
    type="multivec",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1"],
    binSize=5,
)

track = gos.Track(data=data, layout="linear").mark_bar().encode(
    y="peak:Q",
    x="start:G",
    xe="end:G",
    stroke=gos.Channel(value=0.5),
    strokeWidth=gos.Channel(value=0.5),
).properties(width=180)

spec = track.chart(title="Basic Marks: Bar", subtitle="Tutorial Examples")

print(spec.to_json())

# {
#   "subtitle": "Tutorial Examples",
#   "title": "Basic Marks: Bar",
#   "tracks": [
#     {
#       "data": {
#         "binSize": 5,
#         "categories": [
#           "sample 1"
#         ],
#         "column": "position",
#         "row": "sample",
#         "type": "multivec",
#         "url": "https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
#         "value": "peak"
#       },
#       "height": 180,
#       "layout": "linear",
#       "mark": "bar",
#       "stroke": {
#         "value": 0.5
#       },
#       "strokeWidth": {
#         "value": 0.5
#       },
#       "width": 180,
#       "x": {
#         "field": "start",
#         "type": "genomic"
#       },
#       "xe": {
#         "field": "end",
#         "type": "genomic"
#       },
#       "y": {
#         "field": "peak",
#         "type": "quantitative"
#       }
#     }
#   ]
# }
```

```python
spec # render spec in jupyter cell!
```

```python
widget = gos.GoslingWidget(spec) # create widget
widget.spec = new_spec # update view
```
