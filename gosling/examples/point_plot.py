"""
Point Plot
==========
"""
# category: basic marks
import gosling as gos

data = gos.multivec(
    url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1"],
    binSize=5,
)

domain = gos.GenomicDomain(chromosome="1", interval=[1, 30005000])

track = gos.Track(data).mark_point().encode(
    x=gos.X("position:G", domain=domain, axis="bottom"),
    y="peak:Q",
    size="peak:Q",
    color="sample:N",
).properties(layout="linear", width=725, height=180)

track.view(title="Basic Marks: Point", subtitle="Tutorial Examples")
