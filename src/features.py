# src/features.py
from __future__ import annotations
import pandas as pd

def make_features(load_series: pd.Series):
    """
    Convert hourly load time-series into ML-ready features.

    Input:
        load_series: pandas Series indexed by timestamp (hourly load in MW)

    Output:
        X: feature DataFrame
        y: target Series
    """
    df = pd.DataFrame({"load_mw": load_series})

    # time features
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek

    # lag features (past load)
    df["lag_1"] = df["load_mw"].shift(1)
    df["lag_24"] = df["load_mw"].shift(24)     # same hour yesterday
    df["lag_168"] = df["load_mw"].shift(168)   # same hour last week

    # rolling stats (use shift(1) to avoid "peeking" at current value)
    df["rolling_mean_24"] = df["load_mw"].shift(1).rolling(24).mean()
    df["rolling_std_24"] = df["load_mw"].shift(1).rolling(24).std()

    # drop NaNs created by shift/rolling
    df = df.dropna()

    X = df.drop(columns=["load_mw"])
    y = df["load_mw"]
    return X, y


if __name__ == "__main__":
    from src.data import load_opsd_de_load
    series = load_opsd_de_load()["load_mw"]
    X, y = make_features(series)
    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print("\nX head:\n", X.head())
