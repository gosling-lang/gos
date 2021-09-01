import gosling.data as data


def test_data():
    url = "http://localhost:8080/data.csv"
    assert data.csv(url) == {"type": "csv", "url": url}
    assert data.bigwig(url) == {"type": "bigwig", "url": url}
    assert data.beddb(url) == {"type": "beddb", "url": url}
    assert data.vector(url) == {"type": "vector", "url": url}
    assert data.multivec(url) == {"type": "multivec", "url": url}
    assert data.bam(url, indexUrl=url) == {"type": "bam", "url": url, "indexUrl": url}

    values = [{"x": 1, "y": 2}]
    assert data.json(values) == {"type": "json", "values": values}
