# ipygosling

> CAUTION! This project is experimental and requires that you build both the
> schema bindings (`gosling/schema`) and JS static assets (`gosling/static/`).

## Generate source code 

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

spec = gos.Root(
    title="Basic Marks: Bar",
    subtitle="Tutorial Examples",
    tracks=[
        gos.Track(
            layout="linear",
            width=800,
            height=180,
            data=gos.DataDeep(
                url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
                type="multivec",
                row="sample",
                column="position",
                value="peak",
                categories=["sample 1"],
                binSize=5
            ),
            mark="bar",
            y=gos.Channel(field="peak", type="quantitative"),
            x=gos.Channel(field="start", type="genomic"),
            xe=gos.Channel(field="end", type="genomic"),
            stroke=gos.Channel(value=0.5),
            strokeWidth=gos.Channel(value=0.5),
        )
    ]
)

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
#       "width": 800,
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
gos.Gosling(spec) # render spec!
```

```python
widget = gos.GoslingWidget(spec) # create widget
widget.spec = new_spec # update view
```
