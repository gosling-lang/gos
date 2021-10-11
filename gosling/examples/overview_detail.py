"""
Overview + Details
==================
"""
# category: interactive visualizations
import gosling as gos

multivec_data = gos.multivec(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1", "sample 2", "sample 3", "sample 4"],
    binSize=4,
)

rearrangments = gos.csv(
    url="https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/rearrangements.bulk.1639.simple.filtered.pub",
    headerNames=["chr1", "p1s", "p1e", "chr2", "p2s", "p2e", "type", "id", "f1", "f2", "f3", "f4", "f5", "f6"],
    separator="\t",
    genomicFieldsToConvert=[
        {"chromosomeField": "chr1", "genomicFields": ["p1s", "p1e"]},
        {"chromosomeField": "chr2", "genomicFields": ["p2s", "p2e"]},
    ],
)

base = gos.Track(multivec_data).mark_bar(outlineWidth=0).encode(
    x="start:G",
    xe="end:G",
    y="peak:Q",
    row="sample:N",
    color="sample:N",
    stroke=gos.value("black"),
    strokeWidth=gos.value(0.3),
)

circular = gos.stack(
    (
        gos.overlay(
            base.mark_bar(),
            base.mark_brush().encode(
                x=gos.X("start:G", linkingId="detail-1"),
                color=gos.value("blue")
            ),
            base.mark_brush().encode(
                x=gos.X("start:G", linkingId="detail-2"),
                color=gos.value("red")
            ),
        ).properties(width=500, height=100)
    ),
    (
        gos.Track(rearrangments)
            .mark_withinLink()
            .encode(
                x="p1s:G",
                xe="p1e:G",
                x1="p2s:G",
                x1e="p2e:G",
                stroke=gos.Stroke(
                    "type:N",
                    domain=["deletion", "inversion", "translocation", "tandem-duplication"],
                ),
                strokeWidth=gos.value(0.8),
                opacity=gos.value(0.15),
            )
            .transform_filter("chr1", oneOf=["1", "16", "14", "9", "6", "5", "3"])
            .transform_filter("chr2", oneOf=["1", "16", "14", "9", "6", "5", "3"])
            .properties(width=500, height=100)
    ),
).properties(static=True, layout="circular")


def detail(background, linkingId, legend, chromosome):
    domain = gos.GenomicDomain(chromosome=chromosome)
    return base.mark_bar(background=background, backgroundOpacity=0.1).encode(
        x=gos.X("start:G", linkingId=linkingId, domain=domain),
        strokeWidth=gos.value(0.3),
        color=gos.Color("sample:N", legend=legend),
    ).properties(width=245, height=150)

details = gos.horizontal(
    detail("blue", "detail-1", legend=False, chromosome="5"),
    detail("red", "detail-2", legend=True, chromosome="16"),
    spacing=10,
)

gos.vertical(circular, details)
