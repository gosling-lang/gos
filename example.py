import gosling as gos

multivec = gos.DataDeep(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
    type="multivec",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1", "sample 2", "sample 3", "sample 4"],
    binSize=5,
)

base = gos.Track(data=multivec, width=1600, height=130)
tooltip = [
    {"field": "position", "type": "genomic", "alt": "Position"},
    {"field": "peak", "type": "quantitative", "alt": "Value", "format": ".2"},
    {"field": "sample", "type": "nominal", "alt": "Sample"},
]

track1 = base.mark_rect().encode(
    x=gos.Channel("start:G", axis="top"),
    xe="end:G",
    row=gos.Channel("sample:N", legend=True),
    color=gos.Channel("peak:Q", legend=True),
    tooltip=tooltip,
)

track2 = base.mark_bar().encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Channel("sample:N", legend=True),
    tooltip=tooltip,
)

track3 = base.mark_bar().encode(
    x=gos.Channel("position:G", axis="top"),
    y=gos.Channel("peak:Q", grid=True),
    color=gos.Channel("smaple:N", legend=True),
    tooltip=tooltip,
)

track4 = base.encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Channel("sampleN", legend=True),
    tooltip=tooltip,
).properties(
    alignment="overlay",
    tracks=[
        {"mark": "line"},
        {
            "mark": "point",
            "size": {"field": "peak", "type": "quantitative", "range": [0, 2]},
        },
    ],
)

track5 = base.mark_point().encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    size="peak:Q",
    color=gos.Channel("sample:N", legend=True),
    opacity={"value": 0.5},
    tooltip=tooltip,
)

track6 = base.mark_point().encode(
    x=gos.Channel("position:G", axis="top"),
    y=gos.Channel("peak:Q", grid=True),
    size="peak:Q",
    color=gos.Channel("sample:N", legend=True),
    opacity={"value": 0.5},
    tooltip=tooltip,
)

track7 = base.mark_area().encode(
    x=gos.Channel("position:G", axis="top"),
    y="peak:Q",
    row="sample:N",
    color=gos.Channel("sample:N", legend=True),
    stroke={"value": "white"},
    strokeWidth={"value": 0.5},
    tooltip=tooltip,
)

track8 = base.mark_withinLink().encode(
    x=gos.Channel(
        "s1:G", domain=gos.Domain(chromosome="1", interval=[103900000, 104100000])
    ),
    xe="e1:G",
    x1=gos.Channel("s2:G", domain=gos.Domain(chromosome="1")),
    x1e="e2:G",
    color="s1:N",
    stroke={"value": "black"},
    strokeWidth={"value": 0.5},
    opacity={"value": 0.2},
)

spec = gos.Root(
    title="Visual Encoding",
    subtitle="Gosling provides diverse visual encoding methods",
    layout="linear",
    arrangement="vertical",
    centerRadius=0.8,
    xDomain=gos.Domain(chromosome="1", interval=[1, 3000500]),
    views=[
        {"tracks": [track]}
        for track in [
            track1,
            track2,
            track3,
          #  track4,
            track5,
            track6,
            track7,
            track8,
        ]
    ],
)

print(spec.to_json())
