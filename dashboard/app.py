import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]        #gets the project root directory
sys.path.append(str(ROOT_DIR))                        #tells Python: “hey, treat this folder as importable”
import pandas as pd
import streamlit as st





from src.data import load_opsd_de_load

st.set_page_config(page_title="OPSD DE Load Dashboard", layout="wide")

st.title("OPSD Germany Electricity Load Dashboard")
st.caption("Real hourly electricity demand data for Germany (MW) from Open Power System Data (OPSD).")

# Load data
df = load_opsd_de_load().copy()
df = df.sort_index()

# --- KPIs (top row) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", f"{len(df):,}")
col2.metric("Columns", f"{df.shape[1]}")
col3.metric("Start", str(df.index.min()))
col4.metric("End", str(df.index.max()))

st.divider()

# --- Data preview ---
left, right = st.columns([1, 1])

with left:
    st.subheader("Data Preview (Head)")
    n = st.slider("Rows to display", min_value=5, max_value=50, value=10, step=5)
    st.dataframe(df.head(n), use_container_width=True)

with right:
    st.subheader("Dataset Info")
    st.write("**Column(s):**", list(df.columns))
    st.write("**Index type:**", type(df.index).__name__)
    st.write("**Dtype(s):**")
    st.write(df.dtypes)

st.divider()

# --- Summary stats ---
st.subheader("Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)
st.divider()
st.subheader("Interactive Visualizations")

# Controls
colA, colB = st.columns([1, 2])
with colA:
    days = st.slider("Show last N days", min_value=7, max_value=365, value=30, step=7)
with colB:
    st.caption("Tip: Use this to explore daily/weekly patterns and demand peaks.")

# Filter last N days
end = df.index.max()
start = end - pd.Timedelta(days=days)
df_last = df.loc[start:end].copy()

# 1) Time series (last N days)
st.markdown("### 1) Load over time (last N days)")
st.line_chart(df_last["load_mw"], height=320)

# 2) Average by hour of day
st.markdown("### 2) Average load by hour of day")
tmp = df_last.copy()
tmp["hour"] = tmp.index.hour
hourly = tmp.groupby("hour")["load_mw"].mean()
st.line_chart(hourly, height=260)

# 3) Average by day of week
st.markdown("### 3) Average load by day of week")
tmp2 = df_last.copy()
tmp2["dow"] = tmp2.index.dayofweek  # 0=Mon ... 6=Sun
dow = tmp2.groupby("dow")["load_mw"].mean()
dow.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
st.bar_chart(dow, height=260)

st.divider()

# Download button (filtered dataset)
st.subheader("Download Data (Filtered)")
csv = df_last.reset_index().to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"Download last {days} days as CSV",
    data=csv,
    file_name=f"opsd_de_load_last_{days}_days.csv",
    mime="text/csv",
)
