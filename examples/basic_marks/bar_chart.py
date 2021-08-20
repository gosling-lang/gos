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

track = gos.Track(data).mark_bar().encode(
    x="start:G",
    xe="end:G",
    y="peak:Q",
    stroke={"value": "white"},
    strokeWidth={"value": 0.5},
).properties(layout="linear", width=800, height=180)

track.view(title="Basic Marks: Bar", subtitle="Tutorial Examples")
