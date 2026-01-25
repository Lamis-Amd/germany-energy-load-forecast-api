# src/plotting.py
from __future__ import annotations

import io
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # headless backend (works in Docker)

import matplotlib.pyplot as plt


def plot_last_30_days(df: pd.DataFrame) -> bytes:
    """
    Returns a PNG (bytes) for the last 30 days of Germany load.
    Expects df indexed by datetime and containing column 'load_mw'.
    """
    df = df.sort_index()
    end = df.index.max()
    start = end - pd.Timedelta(days=30)
    last_30d = df.loc[start:end]

    fig = plt.figure()
    plt.plot(last_30d.index, last_30d["load_mw"])
    plt.title("Germany Electricity Load (Last 30 Days) - OPSD")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Load (MW)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def plot_avg_by_hour(df: pd.DataFrame) -> bytes:
    """
    Returns a PNG (bytes) for average load by hour of day.
    """
    tmp = df.copy()
    tmp["hour"] = tmp.index.hour
    hourly = tmp.groupby("hour")["load_mw"].mean()

    fig = plt.figure()
    plt.plot(hourly.index, hourly.values)
    plt.title("Average Load by Hour of Day (DE) - OPSD")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Load (MW)")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
