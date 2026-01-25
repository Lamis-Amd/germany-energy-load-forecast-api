# src/anomaly.py
from __future__ import annotations
import pandas as pd
import numpy as np

def zscore_anomalies(series: pd.Series, window: int = 168, z: float = 3.0) -> pd.DataFrame:
    # rolling mean/std
    mu = series.rolling(window).mean()
    sigma = series.rolling(window).std()
    zscore = (series - mu) / sigma
    out = pd.DataFrame({
        "value": series,
        "zscore": zscore,
        "is_anomaly": (zscore.abs() > z)
    }).dropna()
    return out
