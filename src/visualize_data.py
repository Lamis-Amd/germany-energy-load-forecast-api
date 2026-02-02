
import pandas as pd
import matplotlib.pyplot as plt

from src.data import load_opsd_de_load

def main():
    df = load_opsd_de_load()

    # 1) Raw time series (sample: last 30 days)
    df = df.sort_index()
    end = df.index.max()
    start = end - pd.Timedelta(days=30)
    last_30d = df.loc[start:end]
    plt.figure()
    plt.plot(last_30d.index, last_30d["load_mw"])
    plt.title("Germany Electricity Load (Last 30 Days) - OPSD")
    plt.xlabel("Time (UTC)")
    plt.ylabel("Load (MW)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 2) Average load by hour of day
    df["hour"] = df.index.hour
    hourly = df.groupby("hour")["load_mw"].mean()
    plt.figure()
    plt.plot(hourly.index, hourly.values)
    plt.title("Average Load by Hour of Day (DE) - OPSD")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Load (MW)")
    plt.tight_layout()
    plt.show()

    # 3) Average load by day of week
    df["dow"] = df.index.dayofweek
    dow = df.groupby("dow")["load_mw"].mean()
    plt.figure()
    plt.bar(dow.index, dow.values)
    plt.title("Average Load by Day of Week (0=Mon ... 6=Sun)")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Load (MW)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
