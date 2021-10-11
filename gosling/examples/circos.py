"""
Circos
======
"""
# category: others
import gosling as gos

WIDTH = 725

tileset = gos.vector(
    url="https://resgen.io/api/v1/tileset_info/?d=VLFaiSVjTjW6mkbjRjWREA",
    column="position",
    value="peak",
)

cytoband = gos.csv(
    url="https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG38.Human.CytoBandIdeogram.csv",
    chromosomeField="Chromosome",
    genomicFields=["chromStart", "chromEnd"],
)

segdup = gos.csv(
    url="https://raw.githubusercontent.com/vigsterkr/circos/master/data/5/segdup.txt",
    headerNames=["id", "chr", "p1", "p2"],
    chromosomePrefix="hs",
    chromosomeField="chr",
    genomicFields=["p1", "p2"],
    separator=" ",
    longToWideId="id",
)

bars = gos.Track(tileset).mark_bar().encode(
    x=gos.X("position:G", axis="top"),
    y=gos.Y("peak:Q", axis="right"),
    color=gos.value("#EEEDA1"),
).properties(width=WIDTH, height=60)

ideogram = gos.Track(cytoband).mark_rect().encode(
    color=gos.Color("Stain:N",
        domain=["gneg", "gpos25", "gpos50", "gpos75", "gpos100", "gvar", "acen"],
        range=["white", "#D9D9D9", "#979797", "#636363", "black", "#F0F0F0", "#8D8D8D"],
    ),
    x="chromStart:G",
    xe="chromEnd:G",
    stroke=gos.value("lightgray"),
    strokeWidth=gos.value(0.5),
).properties(width=WIDTH, height=30)


link_base = gos.Track(segdup).mark_withinLink().encode(
    x="p1:G",
    xe="p1_2:G",
    x1="p2:G",
    x1e="P2_2:G",
    opacity=gos.value(0.4)
).properties(width=WIDTH, height=300)

colors = ["#E79F00", "#029F73", "#0072B2", "#CB7AA7", "#D45E00", "#57B4E9", "#EFE441"]

link = gos.overlay(
    link_base
        .encode(stroke=gos.value("lightgray"), strokeWidth=gos.value(1))
        .transform_filter_not("chr", oneOf=["hs1"])
    ,
    link_base
        .encode(stroke=gos.Stroke("chr_2:N", range=colors), strokeWidth=gos.value(1.5))
        .transform_filter("chr", oneOf=["hs1"])
)

gos.stack(bars, ideogram, link).properties(
    title="Circos",
    description="http://circos.ca/intro/genomic_data/",
    layout="circular",
    static=True,
    spacing=1,
    centerRadius=0.3,
)
