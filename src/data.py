# src/data.py
from __future__ import annotations
import pandas as pd

# Real dataset page (OPSD): https://data.open-power-system-data.org/time_series/
# We use a fixed versioned URL for stability.
OPSD_URL = (
    "https://data.open-power-system-data.org/time_series/2020-10-06/"
    "time_series_60min_singleindex.csv"
)

def load_opsd_de_load() -> pd.DataFrame:
    """
    Returns a DataFrame indexed by utc_timestamp with one column: load_mw
    (Germany actual load from ENTSO-E Transparency via OPSD).
    """
    df = pd.read_csv(OPSD_URL)

    # Parse time and sort
    df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"], errors="coerce")
    df = df.dropna(subset=["utc_timestamp"]).sort_values("utc_timestamp")

    # Germany actual load column (MW)
    col = "DE_load_actual_entsoe_transparency"
    if col not in df.columns:
        # Helpful debug: show similar columns
        candidates = [c for c in df.columns if "DE_load" in c]
        raise ValueError(f"Column not found: {col}. Available: {candidates[:10]}")

    out = df[["utc_timestamp", col]].rename(columns={col: "load_mw"})
    out = out.dropna(subset=["load_mw"]).set_index("utc_timestamp")

    # Ensure numeric
    out["load_mw"] = pd.to_numeric(out["load_mw"], errors="coerce")
    out = out.dropna(subset=["load_mw"])

    return out

if __name__ == "__main__":
    data = load_opsd_de_load()
    print(data.head())
    print("\nRows:", len(data))
    print("From:", data.index.min(), "To:", data.index.max())
    print("Mean load (MW):", data["load_mw"].mean())
