# api/main.py
from __future__ import annotations

from fastapi.responses import Response
from src.plotting import plot_last_30_days, plot_avg_by_hour


import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from src.data import load_opsd_de_load
from src.features import make_features
from api.schemas import ForecastResponse, ForecastPoint

MODEL_PATH = "models/model.joblib"

app = FastAPI(title="OPSD DE Load Forecast API", version="1.0")


def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Error: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/forecast", response_model=ForecastResponse)
def forecast(horizon_hours: int = 24):
    if horizon_hours < 1 or horizon_hours > 72:
        raise HTTPException(status_code=400, detail="horizon_hours must be between 1 and 72")

    model = load_model()

    # Load real data (history)
    df = load_opsd_de_load()
    ts = df["load_mw"].copy()

    # Forecast iteratively hour-by-hour
    forecast_points = []
    current_ts = ts.copy()

    for _ in range(horizon_hours):
        X, _ = make_features(current_ts)
        x_last = X.iloc[[-1]]
        y_pred = float(model.predict(x_last)[0])

        next_time = current_ts.index[-1] + pd.Timedelta(hours=1)
        forecast_points.append(
            ForecastPoint(timestamp=next_time.isoformat(), load_mw_pred=y_pred)
        )
        current_ts.loc[next_time] = y_pred

    return ForecastResponse(horizon_hours=horizon_hours, forecast=forecast_points)
@app.get("/plots/last30days")
def plots_last_30_days():
    df = load_opsd_de_load()
    png_bytes = plot_last_30_days(df)
    return Response(content=png_bytes, media_type="image/png")


@app.get("/plots/avg-by-hour")
def plots_avg_by_hour():
    df = load_opsd_de_load()
    png_bytes = plot_avg_by_hour(df)
    return Response(content=png_bytes, media_type="image/png")
