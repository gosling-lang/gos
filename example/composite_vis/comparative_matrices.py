import gosling as gos

size = 400
scaled_size = size / 15

# Data

HFFc6_H3K4me3 = gos.Data(
    url="https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_H3K4me3.bigWig",
    type="bigwig",
    column="position",
    value="peak",
    binSize=8,
)

HFFc6_Atacseq = gos.Data(
    url="https://s3.amazonaws.com/gosling-lang.org/data/HFFc6_Atacseq.mRp.clN.bigWig",
    type="bigwig",
    column="position",
    value="peak",
    binSize=8
)

HFFC6_CTCF = gos.Data(
    url="https://s3.amazonaws.com/gosling-lang.org/data/HFFC6_CTCF.mRp.clN.bigWig",
    type="bigwig",
    column="position",
    value="peak",
    binSize=8,
)

genes = gos.Data(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=gene-annotation",
    type="beddb",
    genomicFields=[
        {"index": 1, "name": "start"},
        {"index": 2, "name": "end"},
    ],
    valueFields=[
        {"index": 5, "name": "strand", "type": "nominal"},
        {"index": 3, "name": "name", "type": "nominal"},
    ],
)

matrix_data = gos.Data(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=hffc6-microc-hg38",
    type="matrix",
)

epilogos_data = gos.Data(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=epilogos-hg38",
    type="multivec",
    row="category",
    column="position",
    value="value",
    categories=[
        "Active TSS", "Flanking Active TSS", "Transcr at gene 5\\' and 3\\'",
        "Strong transcription", "Weak transcription", "Genic enhancers",
        "Enhancers", "ZNF genes & repeats", "Heterochromatin",
        "Bivalent/Poised TSS", "Flanking Bivalent TSS/Enh", "Bivalent Enhancer",
        "Repressed PolyComb", "Weak Repressed PolyComb", "Quiescent/Low",
    ],
    binSize=8,
)

# Tracks & Views

track1 = gos.Track(HFFc6_H3K4me3).mark_bar().encode(
    x=gos.Channel("start:G", axis="top"),
    xe="end:G",
    y=gos.Channel("peak:Q", axis="none"),
    color=gos.value("darkgreen"),
).properties(title="HFFc6_H3K4me3", height=size, width=scaled_size)

track2 = gos.Track(HFFc6_Atacseq).mark_bar().encode(
    x="start:G",
    xe="end:G",
    y=gos.Channel("peak:Q", axis="none"),
    color=gos.value("#E79F00"),
).properties(title="HFFc6_ATAC", height=size, width=scaled_size)

gene_anno_base = gos.Track(genes).encode(
    x="start:G",
    size=gos.value(13),
    stroke=gos.value("white"),
    strokeWidth=gos.value(1),
    color=gos.value("#CB7AA7"),
    row=gos.Channel("strand:N", domain=["+", "-"]),
)

gene_overlay = gos.overlay(
    gos.Track(HFFC6_CTCF).mark_bar().encode(
        x="start:G",
        xe="end:G",
        y=gos.Channel("peak:Q", axis="none"),
        color=gos.value("#0072B2")
    ),
    gene_anno_base.mark_triangleRight(backgroundOpacity=0).encode(
        color=gos.value("#CB7AA7"),
    ).properties(
        dataTransform=[{"type": "filter", "field": "strand", "oneOf": ["+"]}],
    ),
    gene_anno_base.mark_triangleLeft(backgroundOpacity=0).encode(
        color=gos.value("#029F73"),
    ).properties(
        title="HFFC6_CTCF",
        dataTransform=[{"type": "filter", "field": "strand", "oneOf": ["-"]}],
    )
).properties(height=size, width=scaled_size)

# Configure Layout

left = gos.stack(track1, track2, gene_overlay).properties(
    orientation="vertical",
    yOffset=size / 3.65,
)

top = gos.stack(
    track1.properties(width=size, height=scaled_size),
    track2.properties(width=size, height=scaled_size),
    gene_overlay.properties(width=size, height=scaled_size),
)

matrix = gos.Track(matrix_data).mark_rect().encode(
    x=gos.Channel("position1:G", axis="none"),
    y=gos.Channel("position2:G", axis="none"),
    color=gos.Channel("value:Q", range="warm"),
).properties(title="HFFc6_Micro-C", width=size, height=size)


bottom = gos.Track(epilogos_data).mark_bar().encode(
    x=gos.Channel("start:G", axis="none"),
    xe="end:G",
    y=gos.Channel("value:Q", axis="none"),
    color=gos.Channel("category:N", range=[
        "#FF0000", "#FF4500", "#32CD32", "#008000", "#006400",
        "#C2E105", "#FFFF00", "#66CDAA", "#8A91D0", "#CD5C5C",
        "#E9967A", "#BDB76B", "#808080", "#C0C0C0", "gray"
    ]),
).properties(
    title="Epilogos (hg38)",
    dataTransform=[{"type": "filter", "field": "value", "inRange": [0, 999999]}],
    width=size,
    height=scaled_size,
)

pane = gos.vertical(top, matrix, bottom, spacing=0)

right = gos.View(views=[pane, pane], spacing=30)

gos.horizontal(left, right).properties(
    title="Matrix Visualization",
    subtitle="Comparison of Micro-C and Hi-C for HFFc6 Cells",
    xDomain=gos.Domain(chromosome="7",
    interval=[77700000, 81000000]),
    spacing=1,
    linkingId="-"
)
