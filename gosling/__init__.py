import pandas as pd

from gosling.schema import *
from gosling.api import *
from gosling.data import (
    GoslingDataServer,
    bam,
    beddb,
    bigwig,
    csv,
    data_server,
    json,
    matrix,
    multivec,
    vector,
)
from gosling.display import themes


@pd.api.extensions.register_dataframe_accessor("gos")  # type: ignore
class GosAccessor:
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def csv(self, **kwargs):
        content = self._df.to_csv(index=False) or ""
        url = data_server(content, extension="csv")
        return dict(type="csv", url=url, **kwargs)
