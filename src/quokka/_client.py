from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

import requests

from ._config import AlphaVantageConfig
from .models import TimeSeriesDataPointModel


class AlphaVantageClient:
    class DataPointInterval(str, Enum):
        INTERVAL_1_MIN = "1min"
        INTERVAL_5_MIN = "5min"
        INTERVAL_15_MIN = "15min"
        INTERVAL_30_MIN = "30min"
        INTERVAL_60_MIN = "60min"

    class DataSize(str, Enum):
        SIZ_COMPACT = "compact"
        SIZE_FULL = "full"

    class ResultDataFormat(str, Enum):
        FORMAT_JSON = "json"
        FORMAT_CSV = "csv"

    class _ApiFunction(str, Enum):
        FUNCTION_TIME_SERIES_INTRADAY = "TIME_SERIES_INTRADAY"

    def __init__(self, *, api_key: str | None = None) -> None:
        self._session = requests.Session()
        self._config = AlphaVantageConfig()
        self._api_key = api_key or self._config.api_key

    def intraday(
        self,
        symbol: str,
        *,
        interval: DataPointInterval = DataPointInterval.INTERVAL_5_MIN,
        adjusted: bool = True,
        extended_hours: bool = True,
        size: DataSize = DataSize.SIZ_COMPACT,
        format: ResultDataFormat = ResultDataFormat.FORMAT_JSON,
    ) -> None:
        """Provide current and over 20 years of historical intraday OHLCV time series data."""
        # Pack params into a dict
        params = {
            "symbol": symbol,
            "interval": interval,
            "adjusted": adjusted,
            "extended_hours": extended_hours,
            "outputsize": size,
            "datatype": format,
        }

        data = self._get(
            function=AlphaVantageClient._ApiFunction.FUNCTION_TIME_SERIES_INTRADAY, params=params
        )
        print(data)

    def _get(self, function: _ApiFunction, params: dict[str, Any]) -> list[TimeSeriesDataPointModel]:
        """Send a HTTP GET request and return the response payload as a dict."""
        params["function"] = function
        params["apikey"] = self._api_key

        url = f"https://{self._config.hostname}/query"
        r = requests.get(url, params=params)
        r.raise_for_status()  # API is not REST standard; does not return != 200 on errors

        payload = r.json()
        if error_message := payload.get("Error Message"):
            raise Exception(f"Server said: {error_message}")

        results = []
        for ts, record in list(payload.values())[1].items():
            results.append(TimeSeriesDataPointModel.load(datetime.fromisoformat(ts).timestamp(), record))

        return results
