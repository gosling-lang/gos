"""
Ideograms
=========
"""
# category: composite visualizations
import gosling as gos

def ideogram_with_bars(chromosome: str, width: int):
    """
    Ideograms
    """
    data = gos.csv(
        url="https://raw.githubusercontent.com/sehilyi/gemini-datasets/master/data/UCSC.HG38.Human.CytoBandIdeogram.csv",
        chromosomeField="Chromosome",
        genomicFields=["chromStart", "chromEnd"],
    )

    arms = gos.Track(data).mark_rect().encode(
        color=gos.Color("Stain:N",
            domain=["gneg", "gpos25", "gpos50", "gpos75", "gpos100", "gvar"],
            range=["white", "#D9D9D9", "#979797", "#636363", "black", "#A0A0F2"],
        ),
        x=gos.X("chromStart:G", axis="none"),
        xe="chromEnd:G",
        stroke=gos.value("black"),
        strokeWidth=gos.value(0.5),
    ).transform_filter_not("Stain", oneOf=["acen"])

    arm_labels = arms.mark_text().encode(
        text="Name:N",
        color=gos.Color("Stain:N",
            domain=["gneg", "gpos25", "gpos50", "gpos75", "gpos100", "gvar"],
            range=["black", "#636363", "black", "#D9D9D9", "white", "black"],
        ),
        strokeWidth=gos.value(0)
    ).visibility_lt(
        target='mark',
        measure='width',
        threshold='|xe-x|',
        transitionPadding=10
    )

    centromere_base = gos.Track(data).encode(
        x=gos.X("chromStart:G"),
        xe="chromEnd:G",
        color=gos.value('red'),
    ).transform_filter(
        "Stain", oneOf=["acen"]
    )

    centromere_1 = centromere_base.mark_triangleLeft().transform_filter(
        "Name", include="p"
    )

    centromere_2 = centromere_base.mark_triangleRight().transform_filter(
        "Name", include="q"
    )

    ideogram = gos.overlay(arms, arm_labels, centromere_1, centromere_2).properties(width=width, height=20)

    """
    Stacked Bar Charts
    """
    mvdata = gos.multivec(
        url="https://server.gosling-lang.org/api/v1/tileset_info/?d=cistrome-multivec",
        row="sample",
        column="position",
        value="peak",
        categories=["sample 1", "sample 2"],
        binSize=2,
    )

    bar = gos.Track(mvdata).mark_bar().encode(
        x="start:G",
        xe="end:G",
        y="peak:Q",
        color=gos.Color("sample:N"),
    ).properties(width=width, height=20)

    return gos.stack(bar, ideogram).properties(
        xDomain=gos.GenomicDomain(chromosome=chromosome),
        spacing=0
    )

"""
Composition
"""
gos.parallel(
    ideogram_with_bars("1", 1000),
    ideogram_with_bars("2", 970),
    ideogram_with_bars("3", 800),
    ideogram_with_bars("4", 770),
    ideogram_with_bars("5", 740)
).properties(
    static=True
)
