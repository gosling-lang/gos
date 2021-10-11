import pytest

import gosling as gos


@pytest.fixture
def basic_track() -> gos.Track:
    data = gos.Data(
        url="http://localhost:8080/data.csv",
        type="csv",
        chromosomeField="Chromosome",
        genomicFields=["chromStart", "chromEnd"],
    )
    return (
        gos.Track(data)
        .mark_line()
        .encode(
            x=gos.X("position:G", axis="top"),
            y="peak:Q",
        )
    )


def test_value() -> None:
    assert gos.value(1) == {"value": 1}
    assert gos.value("hello") == {"value": "hello"}


def test_basic_view(basic_track: gos.Track) -> None:
    view = basic_track.view()
    assert isinstance(view, gos.View)
    assert view.to_dict() == {"tracks": [basic_track.to_dict()]}


def test_transforms(basic_track: gos.Track) -> None:
    # filter transform
    track = basic_track.transform_filter("position", oneOf=["+"])
    kwds = dict(type="filter", field="position", oneOf=["+"])
    assert track.dataTransform == [gos.FilterTransform(**kwds)]
    assert not isinstance(basic_track.dataTransform, list)

    # filter transform not
    track = basic_track.transform_filter_not("position", oneOf=["+"])
    kwds = {"type": "filter", "field": "position", "not": True, "oneOf": ["+"]}
    assert track.dataTransform == [gos.FilterTransform(**kwds)]

    # transform log
    track = basic_track.transform_log("peak")
    kwds = {"type": "log", "field": "peak"}
    assert track.dataTransform == [gos.LogTransform(**kwds)]

    # transform string concat
    track = basic_track.transform_str_concat(
        ["position", "peak"], newField="z", separator="-"
    )
    kwds = dict(type="concat", fields=["position", "peak"], newField="z", separator="-")
    assert track.dataTransform == [gos.StrConcatTransform(**kwds)]

    # transform string replace
    replace = [{"from": "x", "to": "y"}]
    track = basic_track.transform_str_replace("position", newField="z", replace=replace)
    kwds = dict(type="replace", field="position", newField="z", replace=replace)
    assert track.dataTransform == [gos.StrReplaceTransform(**kwds)]

    # transform displace
    bounding_box = {"startField": "peak", "endField": "peak"}
    track = basic_track.transform_displace(
        boundingBox=bounding_box, newField="z", method="pile"
    )
    kwds = dict(type="displace", boundingBox=bounding_box, newField="z", method="pile")
    assert track.dataTransform == [gos.DisplaceTransform(**kwds)]

    # transform exon split
    field = dict(field="peak", type="quantitative", newField="z", chrField="position")
    track = basic_track.transform_exon_split(
        separator="-", flag={"field": "peak", "value": 10}, fields=[field]
    )
    kwds = dict(
        type="exonSplit",
        separator="-",
        flag={"field": "peak", "value": 10},
        fields=[field],
    )
    assert track.dataTransform == [gos.ExonSplitTransform(**kwds)]

    # transform coverage
    track = basic_track.transform_coverage("x", "xe")
    kwds = dict(type="coverage", startField="x", endField="xe")
    assert track.dataTransform == [gos.CoverageTransform(**kwds)]

    # transform json parse
    track = basic_track.transform_json_parse(
        "z", baseGenomicField="x", genomicField="xx", genomicLengthField="xxx"
    )
    kwds = dict(
        type="subjson",
        field="z",
        baseGenomicField="x",
        genomicField="xx",
        genomicLengthField="xxx",
    )
    assert track.dataTransform == [gos.JSONParseTransform(**kwds)]


def test_chained_transforms(basic_track: gos.Track) -> None:
    track = basic_track.transform_filter("position", oneOf=["+"]).transform_filter_not(
        "position", oneOf=["-"]
    )
    assert not isinstance(basic_track.dataTransform, list)
    assert len(track.dataTransform) == 2
    assert "not" in track.dataTransform[1].to_dict()


def test_visibilities(basic_track: gos.Track) -> None:
    track = basic_track.visibility_lt(target="track", measure="width", threshold=10)
    kwds = dict(operation="LT", target="track", measure="width", threshold=10)
    assert track.visibility == [gos.VisibilityCondition(**kwds)]

    track = basic_track.visibility_gt(target="track", measure="width", threshold=10)
    kwds = dict(operation="GT", target="track", measure="width", threshold=10)
    assert track.visibility == [gos.VisibilityCondition(**kwds)]

    track = basic_track.visibility_le(target="track", measure="width", threshold=10)
    kwds = dict(operation="LTET", target="track", measure="width", threshold=10)
    assert track.visibility == [gos.VisibilityCondition(**kwds)]

    track = basic_track.visibility_ge(target="track", measure="width", threshold=10)
    kwds = dict(operation="GTET", target="track", measure="width", threshold=10)
    assert track.visibility == [gos.VisibilityCondition(**kwds)]


def test_track_composition(basic_track: gos.Track) -> None:
    view = gos.overlay(basic_track.properties(width=500, height=10), basic_track)
    assert isinstance(view, gos.View)
    assert view.alignment == "overlay"
    # uses width and height from first track
    assert view.width == 500
    assert view.height == 10
    assert len(view.tracks) == 2

    # override w/h at view-level
    view = gos.overlay(
        basic_track.properties(width=500, height=10),
        basic_track.properties(width=10, height=40),
        basic_track,
        width=60,
        height=60,
    )
    assert view.width == 60
    assert view.height == 60
    assert len(view.tracks) == 3
    for track in view.tracks:
        assert track.width == gos.Undefined
        assert track.height == gos.Undefined

    view = gos.stack(
        basic_track.properties(width=50, height=50),
        basic_track.properties(width=60, height=60),
    )
    assert isinstance(view, gos.View)
    assert view.alignment == "stack"
    assert len(view.tracks) == 2


def test_view_composition(basic_track: gos.Track) -> None:

    view = gos.horizontal(basic_track.view(), basic_track.view())
    assert isinstance(view, gos.View)
    assert view.arrangement == "horizontal"
    assert len(view.views) == 2

    view = gos.vertical(basic_track.view(), basic_track.view())
    assert isinstance(view, gos.View)
    assert view.arrangement == "vertical"
    assert len(view.views) == 2

    view = gos.serial(basic_track.view(), basic_track.view())
    assert isinstance(view, gos.View)
    assert view.arrangement == "serial"
    assert len(view.views) == 2

    view = gos.parallel(basic_track.view(), basic_track.view())
    assert isinstance(view, gos.View)
    assert view.arrangement == "parallel"
    assert len(view.views) == 2

    # works with both tracks and views
    view = gos.serial(
        basic_track.view(),
        basic_track,
        basic_track,
        basic_track.view(),
    )
    assert isinstance(view, gos.View)
    assert len(view.views) == 4
    for v in view.views:
        assert isinstance(v, gos.View)
