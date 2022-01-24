import pathlib
from typing import Any

import pandas as pd
import pytest

from gosling.api import Data
from gosling.data import csv, data_server


@pytest.fixture(scope="function")
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


def test_df_extension(session_context: Any):
    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [1, 2, 3, 4, 5],
            "cat": ["a", "b", "c", "d", "e"],
        }
    )
    assert hasattr(df, "gos")
    data = df.gos.csv()
    assert "localhost" in data["url"]
    assert data["type"] == "csv"
    assert len(data_server._resources) == 1


def test_missing_files(tmpdir: pytest.Testdir, session_context: Any):
    data_dir = pathlib.Path(tmpdir.mkdir("data"))
    tmp = data_dir / "data.csv"

    # returns if passed a string
    data = csv(url=str(tmp))
    assert isinstance(Data(**data), Data)
    assert "localhost" not in data["url"]
    assert isinstance(data["url"], str)
