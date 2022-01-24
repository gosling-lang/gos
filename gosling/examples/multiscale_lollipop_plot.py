"""
Multiscale Lollipop Plot
========================
"""
# category: interactive visualizations
import gosling as gos
 
clin_var_beddb = gos.beddb(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=clinvar-beddb",
    genomicFields=[{"index": 1, "name": "start"}, {"index": 2, "name": "end"}],
    valueFields=[{"index": 7, "name": "significance", "type": "nominal"}],
)

categories = [
    "Benign", "Benign/Likely_benign", "Likely_benign", 
    "Uncertain_significance", "Likely_pathogenic", 
    "Pathogenic/Likely_pathogenic", "Pathogenic",
]

colors = ["#5A9F8C", "#5A9F8C", "#029F73", "gray", "#CB96B3", "#CB71A3", "#CB3B8C"]

clin_var_multivec = gos.multivec(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=clinvar-multivec",
    row="significance",
    column="position",
    value="count",
    categories=categories,
    binSize=4,
)


lolipop = gos.overlay(
    (
        gos.Track(clin_var_beddb).mark_bar().encode(
            x="start:G",
            y=gos.Y("significance:N", domain=categories, range=[150, 20], baseline="Uncertain_significance"),
            size=gos.value(1),
            color=gos.value("lightgray"),
            stroke=gos.value("lightgray"),
            strokeWidth=gos.value(1),
            opacity=gos.value(0.3),
        ).visibility_lt(
            measure="zoomLevel",
            target="mark",
            threshold=100000,
            transitionPadding=100000,
        )
    ),
    (
        gos.Track(clin_var_beddb).mark_point().encode(
            x="start:G",
            color=gos.Color("significance:N", domain=categories, range=colors),
            row=gos.Row("significance:N", domain=categories),
            size=gos.value(7),
            opacity=gos.value(0.8),
        ).visibility_lt(
            measure="zoomLevel",
            target="mark",
            threshold=1000000,
            transitionPadding=1000000,
        )
    ),
    (
        gos.Track(clin_var_multivec).mark_bar().encode(
            x="start:G",
            xe="end:G",
            y=gos.Y("count:Q", axis="none"),
            color=gos.Color("significance:N", domain=categories, range=colors, legend=True)
        ).visibility_gt(
            measure="zoomLevel",
            target="mark",
            threshold=500000,
            transitionPadding=500000,
        )
    ),
    width=725,
    height=150,
    xDomain=gos.GenomicDomain(chromosome="13", interval=[31500000, 33150000]),
)

lolipop
