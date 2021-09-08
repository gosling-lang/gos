"""
Multiscale Sequence Plot
========================
"""
# category: interactive visualizations
import gosling as gos
from gosling.data import multivec

data = multivec(
    url="https://server.gosling-lang.org/api/v1/tileset_info/?d=sequence-multivec",
    row="base",
    column="position",
    value="count",
    categories=["A", "T", "G", "C"]
)

text = gos.Track(data).mark_text().encode(
    x="start:G",
    xe="end:G",
    size=gos.value(24),
    color=gos.value("white"),
    text="base:N",
).visibility_lt(
    measure="width", threshold="|xe-x|", transitionPadding=30, target="mark"
).visibility_lt(
    measure="zoomLevel", threshold=10, target="track"
).transform_filter_not("count", oneOf=[0])

bar = gos.Track(data).mark_bar().encode(
    x="position:G",
    y=gos.Channel("count:Q", axis="none"),
    color=gos.Channel("base:N", domain=["A", "T", "G", "C"], legend=True)
)

gos.overlay(bar, text).properties(
    title="Multi-Scale Sequence Plot",
    xDomain=gos.Domain(interval=[1000000, 1000010]),
    width=725,
    height=100
)
