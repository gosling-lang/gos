import gosling as gos

data = gos.Data(
    url="https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG38.Human.CytoBandIdeogram.csv",
    type="csv",
    chromosomeField="Chromosome",
    genomicFields=["chromStart", "chromEnd"],
)

track = gos.Track(data).mark_rect(outline="white").encode(
    color=gos.Channel("Stain:N",
        domain=["gneg", "gpos25", "gpos50", "gpos75", "gpos100", "gvar"],
        range=["white", "#D9D9D9", "#979797", "#636363", "black", "#A0A0F2"],
    ),
    x=gos.Channel("chromStart:G", domain=gos.Domain(chromosome="1"), axis="top"),
    xe="chromEnd:G",
    size={"value": 20},
    stroke={"value": "gray"},
    strokeWidth={"value": 0.5},
).properties(
    width=800,
    height=40,
    dataTransform=[
        {"type": "filter", "field": "Stain", "oneOf": ["acen"], "not": True}
    ],
)

track.view(title="Basic Marks: Rect", subtitle="Tutorial Examples")
