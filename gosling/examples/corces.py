"""
Single-cell Epigenomic Analysis
===============================

`Corces et al. 2020`_

.. _Corces et al. 2020: https://www.nature.com/articles/s41588-020-00721-x
"""
# category: others
import gosling as gos

WIDTH = 600

# DATA

cytogenetic_band = gos.csv(
    url="https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/cytogenetic_band.csv",
    chromosomeField="Chr.",
    genomicFields=["ISCN_start", "ISCN_stop", "Basepair_start", "Basepair_stop"],
)

gene_anno = gos.beddb(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation",
    genomicFields=[{"index": 1, "name": "start"}, {"index": 2, "name": "end"}],
    valueFields=[
        {"index": 5, "name": "strand", "type": "nominal"},
        {"index": 3, "name": "name", "type": "nominal"}
    ],
    exonIntervalFields=[{"index": 12, "name": "start"}, {"index": 13, "name": "end"}],
)

# TRACKS

ideo_base = gos.Track(cytogenetic_band).mark_rect(outlineWidth=1).encode(
    x=gos.X("Basepair_start:G", axis="none"),
    xe="Basepair_stop:G",
    stroke=gos.value("black"),
    strokeWidth=gos.value(1),
)

ideogram = gos.overlay(
    ideo_base.encode(
        color=gos.Color("Density:N",
            domain=["", "25", "50", "75", "100"],
            range=["white", "#D9D9D9", "#979797", "#636363", "black"]
        ),
        size=gos.value(20),
    ).transform_filter_not("Stain", oneOf=["acen-1", "acen-2"]),
    ideo_base.encode(
        color=gos.value("#A0A0F2"),
        size=gos.value(20),
    ).transform_filter("Stain", oneOf=["gvar"]),
    ideo_base.mark_triangleRight().encode(
        color=gos.value("#B40101"),
        size=gos.value(20),
    ).transform_filter("Stain", oneOf=["acen-1"]),
    ideo_base.mark_triangleLeft().encode(
        color=gos.value("#B40101"),
        size=gos.value(20)
    ).transform_filter("Stain", oneOf=["acen-2"]),
    ideo_base.mark_brush().encode(
        x={"linkingId": "detail"},
        color=gos.value("red"),
        opacity=gos.value(1),
        strokeWidth=gos.value(1),
        stroke=gos.value("red"),
    )
).properties(title="chr3", width=WIDTH, height=25)

gene_base = gos.Track(gene_anno).encode(
    color=gos.Color("strand:N", domain=["+", "-"], range=["#012DB8", "#BE1E2C"]),
    row=gos.Row("strand:N", domain=["+", "-"]),
).visibility_lt(
    measure="width",
    threshold="|xe-x|",
    transitionPadding=10,
    target="mark",
)
genes = gos.overlay(
    gene_base
        .mark_text(textFontSize=8, dy=-12, outline="#20102F")
        .encode(text="name:N", x="start:G", xe="end:G", size=gos.value(8))
        .transform_filter("type", oneOf=["gene"])
        .transform_filter("strand", oneOf=["+"]),
    gene_base
        .mark_text(textFontSize=8, dy=10, outline="#20102F")
        .encode(text="name:N", x="start:G", xe="end:G", size=gos.value(8))
        .transform_filter("type", oneOf=["gene"])
        .transform_filter("strand", oneOf=["-"]),
    gene_base
        .mark_rect(outline="#20102F")
        .encode(x="end:G", size=gos.value(7))
        .transform_filter("type", oneOf=["gene"])
        .transform_filter("strand", oneOf=["+"]),
    gene_base
        .mark_rect(outline="#20102F")
        .encode(x="start:G", size=gos.value(7))
        .transform_filter("type", oneOf=["gene"])
        .transform_filter("strand", oneOf=["-"]),
    gene_base
        .mark_rect(outline="#20102F")
        .encode(x="start:G", xe="end:G", size=gos.value(14))
        .transform_filter("type", oneOf=["exon"]),
    gene_base
        .mark_rule(outline="#20102F")
        .encode(x="start:G", xe="end:G", strokeWidth=gos.value(3))
        .transform_filter("type", oneOf=["exon"]),
)

def bar(title: str, color: str, file: str) -> gos.Track:
    url = f"https://s3.amazonaws.com/gosling-lang.org/data/{file}"
    data = gos.bigwig(url, column="position", value="peak")
    return gos.Track(data).mark_bar(outline="#20102F").encode(
        x="position:G",
        y=gos.Y("peak:Q", axis="right"),
        color=gos.value(color),
    ).properties(title=title, width=WIDTH, height=40)

def link(tileset_id: str, stroke: str) -> gos.Track:
    url = f"https://server.gosling-lang.org/api/v1/tileset_info/?d={tileset_id}"
    data = gos.beddb(url, genomicFields=[{"name": "start", "index": 1}, {"name": "end", "index": 2}])
    return gos.Track(data).mark_withinLink().encode(
        x="start:G",
        xe="end:G",
        y={"flip": True},
        strokeWidth=gos.value(1),
        color=gos.value("none"),
        stroke=gos.value(stroke),
        opacity=gos.value(0.1),
    )

tracks = [
    bar("Excitatory neurons", "#F29B67", "ExcitatoryNeurons-insertions_bin100_RIPnorm.bw"),
    bar("Inhibitory neurons", "#3DC491", "InhibitoryNeurons-insertions_bin100_RIPnorm.bw"),
    bar("Dopaminergic neurons", "#565C8B", "DopaNeurons_Cluster10_AllFrags_projSUNI2_insertions_bin100_RIPnorm.bw"),
    bar("Microglia", "#77C0FA", "Microglia-insertions_bin100_RIPnorm.bw"),
    bar("Oligodendrocytes", "#9B46E5", "Oligodendrocytes-insertions_bin100_RIPnorm.bw"),
    bar("Astrocytes", "#D73636", "Astrocytes-insertions_bin100_RIPnorm.bw"),
    bar("OPCs", "#E38ADC", "OPCs-insertions_bin100_RIPnorm.bw"),
    genes.properties(title="Genes", width=WIDTH, height=80),
    gos.overlay(
        link("oligodendrocyte-plac-seq-bedpe", "#F97E2A"),
        link("microglia-plac-seq-bedpe", "#50ADF9"),
        link("neuron-plac-seq-bedpe", "#7B0EDC"),
    ).properties(title="PLAC-seq (H3K4me3) Nott et al.", width=WIDTH, height=60)
]

# COMPOSE

gos.vertical(
    gos.View(layout="linear", tracks=[ideogram], centerRadius=0.8, xDomain=gos.GenomicDomain(chromosome="3")),
    gos.View(tracks=tracks, linkingId="detail", xDomain=gos.GenomicDomain(chromosome="3", interval=[52168000, 52890000])),
)
