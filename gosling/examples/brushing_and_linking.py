"""
Brushing and Linking
====================
"""
# category: basic marks
import gosling as gos
from gosling.data import multivec

mv = multivec(
    url="https://resgen.io/api/v1/tileset_info/?d=UvVPeLHuRDiYA3qwFlm7xQ",
    row="sample",
    column="position",
    value="peak",
    categories=["sample 1"],
)

base = gos.Track(mv).encode(y="peak:Q").properties(width=800, height=200)

gos.stack(
    gos.overlay(
        base.mark_line().encode(
            x=gos.Channel("position:G", domain=gos.Domain(chromosome="1"), axis="top")
        ),
        base.mark_brush().encode(
            x=gos.Channel(
                "position:G",
                domain=gos.Domain(chromosome="1"),
                axis="top",
                linkingId="linking-with-brush"
            ),
            color=gos.value("steelBlue")
        ),
    ),
    base.mark_line(background="steelBlue", backgroundOpacity=0.1).encode(
        x=gos.Channel(
            "position:G",
            domain=gos.Domain(chromosome="1", interval=[200000000, 220000000]),
            axis="top",
            linkingId="linking-with-brush",
        )
    )
)
