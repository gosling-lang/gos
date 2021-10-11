"""
Gene Annotation
===============

Re-implementation of `Higlass gene-annotations track`_

.. _Higlass gene-annotations track: https://docs.higlass.io/track_types.html#gene-annotations
"""
# category: composite visualizations
import gosling as gos

genes = gos.beddb(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation",
    genomicFields=[
      {"index": 1, "name": "start"},
      {"index": 2, "name": "end"}
    ],
    valueFields=[
      {"index": 5, "name": "strand", "type": "nominal"},
      {"index": 3, "name": "name", "type": "nominal"}
    ],
    exonIntervalFields=[
      {"index": 12, "name": "start"},
      {"index": 13, "name": "end"}
    ]
)

base = gos.Track(genes).encode(
    row=gos.Row("strand:N", domain=["+", "-"]),
    color=gos.Color("strand:N", domain=["+", "-"], range=["#7585FF", "#FF8A85"]),
    tooltip=[
        gos.Tooltip(field="start", type="genomic", alt="Start Position"),
        gos.Tooltip(field="end", type="genomic", alt="End Position"),
        gos.Tooltip(field="strand", type="nominal", alt="Strand"),
        gos.Tooltip(field="name", type="nominal", alt="Name")
    ]
).properties(
    title="Genes | hg38",
)

plusGeneHead = base.mark_triangleRight(align="left").encode(
    x=gos.X("end:G", axis="top"),
    size=gos.value(15)
).transform_filter(
    field="type", oneOf=["gene"]
).transform_filter(
    field="strand", oneOf=["+"]
)

minusGeneHead = base.mark_triangleLeft(align="right").encode(
    x=gos.X("start:G", axis="top"),
    size=gos.value(15)
).transform_filter(
    field="type", oneOf=["gene"]
).transform_filter(
    field="strand", oneOf=["-"]
)

geneLabel = base.mark_text(dy=15).encode(
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    text="name:N",
    size=gos.value(15)
).transform_filter(
    field="type", oneOf=["gene"]
).visibility_lt(
    measure="width",
    threshold="|xe-x|",
    transitionPadding=10,
    target="mark",
)

exon = base.mark_rect().encode(
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    size=gos.value(15)
).transform_filter(
    field="type", oneOf=["exon"]
)

plusGeneRange = base.mark_rule(linePattern={"type": "triangleRight", "size": 5}).encode(
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    strokeWidth=gos.value(3),
).transform_filter(
    field="type", oneOf=["gene"]
).transform_filter(
    field="strand", oneOf=["+"]
)

minusGeneRange = base.mark_rule(linePattern={"type": "triangleLeft", "size": 5}).encode(
    x=gos.X("start:G", axis="top"),
    xe="end:G",
    strokeWidth=gos.value(3),
).transform_filter(
    field="type", oneOf=["gene"]
).transform_filter(
    field="strand", oneOf=["-"]
)

gos.overlay(
    plusGeneRange, minusGeneRange, exon, plusGeneHead, minusGeneHead, geneLabel
).properties(
    width=725, height=100,
    title="Gene Annotation",
    xDomain=gos.GenomicDomain(chromosome="1", interval=[103400000, 103700000]),
    assembly="hg38",
    layout="linear",
    centerRadius=0.7,
)
