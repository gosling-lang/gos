import pathlib
import tempfile
from typing import Iterator

import pytest
import requests
import starlette.requests
import starlette.responses
import starlette.routing

from gosling.data._provider import Provider, Resource, TilesetResource
from gosling.data._tilesets import Tileset

content = b"root content"


class ProviderSubclass(Provider):
    """Test class for Provider subclassing"""

    def _routes(self) -> list:
        routes = super()._routes()
        endpoint = lambda _: starlette.responses.Response(content)
        return [starlette.routing.Route("/", endpoint=endpoint)] + routes


@pytest.fixture(scope="module")
def provider() -> Iterator[Provider]:
    provider = Provider()
    yield provider
    provider.stop()


@pytest.fixture(scope="module")
def provider_subclass() -> Iterator[Provider]:
    provider = ProviderSubclass().start()
    yield provider
    provider.stop()


def test_content_resource(provider: Provider) -> None:
    content = "testing content resource"
    resource = provider.create(content=content, extension="txt")
    assert isinstance(resource, Resource)
    assert resource.url.endswith("txt")
    assert requests.get(resource.url).content.decode() == content


def test_content_default_url(provider: Provider) -> None:
    content = "testing default url"
    resource1 = provider.create(content=content, extension="txt")
    resource2 = provider.create(content=content, extension="txt")
    path = resource1.url.split("/")[-1]
    assert path.endswith(".txt")
    assert len(path) > 4
    assert resource1.url == resource2.url


@pytest.mark.parametrize("route", ["/content", "hello_world.txt", ""])
def test_content_route(provider: Provider, route: str) -> None:
    content = f"testing route {route!r}"
    resource = provider.create(content=content, route=route)
    assert resource.url.split("/")[-1] == route.lstrip("/")
    assert requests.get(resource.url).content == content.encode()


def test_file_resource(provider: Provider) -> None:
    content = b"file content"
    with tempfile.NamedTemporaryFile(suffix=".txt") as f:
        f.write(content)
        f.flush()
        resource = provider.create(filepath=pathlib.Path(f.name))
        assert isinstance(resource, Resource)
        assert requests.get(resource.url).content == content


def test_file_resource_range_request(provider: Provider) -> None:
    content = b"hello, world. some additional content."
    with tempfile.NamedTemporaryFile(suffix=".txt") as f:
        f.write(content)
        f.flush()
        resource = provider.create(filepath=pathlib.Path(f.name))
        assert isinstance(resource, Resource)
        res = requests.get(resource.url, headers={"Range": "bytes=0-12"})
        assert res.status_code == 206
        assert res.content == b"hello, world."


def test_tileset_resource(provider: Provider) -> None:
    tileset = Tileset(
        filepath=pathlib.Path("mock.tiles"),
        tiles=lambda tids: [(tid, None) for tid in tids],
        info=lambda: "tile_info",
    )
    resource = provider.create(tileset=tileset)
    assert isinstance(resource, TilesetResource)
    info = requests.get(resource.url).json()
    assert info[resource.guid] == "tile_info"
    tile_url = resource.url.replace("tileset_info", "tiles") + ".0.0"
    tiles = requests.get(tile_url).json()
    assert f"{resource.guid}.0.0" in tiles


def test_provider_subclass(provider_subclass: Provider) -> None:
    url = provider_subclass.url
    content = requests.get(url).content
    assert content == b"root content"


def test_expected_404(provider: Provider) -> None:
    resource = provider.create(content="some new content")
    url = resource.url + ".html"
    response = requests.get(url)
    assert response.ok == False
    assert response.status_code == 404
