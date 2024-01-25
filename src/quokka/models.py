"""Data models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

TimeSeriesDataPointDataType = TypedDict(
    "TimeSeriesDataPointDataType",
    {
        "1. open": float,
        "2. high": float,
        "3. low": float,
        "4. close": float,
        "5. volume": int,
    },
)


@dataclass
class TimeSeriesDataPointModel:
    """Models tie series data point."""

    timestamp: float
    open: float
    high: float
    low: float
    close: float
    volume: int

    @classmethod
    def load(cls, timestamp: float, data: TimeSeriesDataPointDataType) -> TimeSeriesDataPointModel:
        """Create and return a `TimeSeriesDataPointModel` instance containing the given data."""
        return TimeSeriesDataPointModel(
            timestamp=timestamp,
            open=data["1. open"],
            high=data["2. high"],
            low=data["3. low"],
            close=data["4. close"],
            volume=data["5. volume"],
        )


__all__ = ["TimeSeriesDataPointModel"]
