import pathlib
from typing import Any

import pytest

from gosling.api import Data
from gosling.experimental.data import csv, data_server
from gosling.schemapi import SchemaValidationError


@pytest.fixture(scope="session")
def session_context(request: pytest.Session) -> None:
    # Reset the server at the end of the session.
    request.addfinalizer(data_server.reset)


def test_creates_no_resources(tmpdir: pytest.Testdir, session_context: Any):
    data = csv(url="http://localhost:8000/data.csv")
    assert data["url"] == "http://localhost:8000/data.csv"
    assert data["type"] == "csv"
    assert len(data_server._resources) == 0

    data = csv(url=str(tmpdir.mkdir("data").join("data.csv")))
    assert "url" in data
    assert isinstance(data["url"], str)
    assert data["type"] == "csv"
    assert len(data_server._resources) == 0


def test_creates_resources(tmpdir: pytest.Testdir, session_context: Any):
    data_dir = pathlib.Path(tmpdir.mkdir("data"))

    tmp1 = data_dir / "data1.csv"
    tmp2 = data_dir / "data2.csv"
    tmp3 = data_dir / "data3.csv"

    tmp1.touch()
    tmp2.touch()

    # should only create one resource for same file
    for file in [str(tmp1), tmp1, tmp1]:
        data = csv(url=file)
        assert "localhost" in data["url"]
        assert data["type"] == "csv"
        assert len(data_server._resources) == 1

    data = csv(url=str(tmp2))
    assert "localhost" in data["url"]
    assert data["type"] == "csv"
    assert len(data_server._resources) == 2

    # doesn't add new resource
    csv(url=tmp3)
    assert len(data_server._resources) == 2


def test_missing_files(tmpdir: pytest.Testdir, session_context: Any):
    data_dir = pathlib.Path(tmpdir.mkdir("data"))
    tmp = data_dir / "data.csv"

    # throws if passed a pathlib path
    with pytest.raises(SchemaValidationError):
        Data(**csv(url=tmp))

    # returns if passed a string
    data = csv(url=str(tmp))
    assert isinstance(Data(**data), Data)
    assert "localhost" not in data["url"]
    assert isinstance(data["url"], str)
