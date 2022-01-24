"""
Text Marks
==========
"""
# category: basic marks
import gosling as gos

data = gos.multivec(
    url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
    row="base",
    column="position",
    value="count",
    categories=["A", "T", "G", "C"],
    start="start",
    end="end",
    binSize=16,
)

track = gos.Track(data).mark_text(textStrokeWidth=0).encode(
    y="count:Q",
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    color=gos.Color("base:N", domain=["A", "T", "G", "C"]),
    text="base:N",
).properties(width=725, height=180, stretch=True)

track.view(title="Basic Marks: Text", subtitle="Tutorial Examples")
