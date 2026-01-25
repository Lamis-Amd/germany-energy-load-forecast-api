# src/train.py
from __future__ import annotations

import os
import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.data import load_opsd_de_load
from src.features import make_features

MODEL_PATH = "models/model.joblib"


def main():
    # 1) Load real OPSD Germany load data
    df = load_opsd_de_load()
    series = df["load_mw"]

    # 2) Create features
    X, y = make_features(series)

    # 3) Define a simple, strong baseline model
    model = Pipeline([
        ("scaler", StandardScaler(with_mean=False)),
        ("ridge", Ridge(alpha=1.0))
    ])

    # 4) Time-series cross-validation (quick and honest evaluation)
    tscv = TimeSeriesSplit(n_splits=3)
    maes, rmses = [], []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(X), start=1):
        Xtr, Xte = X.iloc[train_idx], X.iloc[test_idx]
        ytr, yte = y.iloc[train_idx], y.iloc[test_idx]

        model.fit(Xtr, ytr)
        pred = model.predict(Xte)

        mae = mean_absolute_error(yte, pred)
        rmse = np.sqrt(mean_squared_error(yte, pred))
        maes.append(mae)
        rmses.append(rmse)

        print(f"Fold {fold}: MAE={mae:.2f} MW | RMSE={rmse:.2f} MW")

    print("\nAverage:")
    print(f"MAE={np.mean(maes):.2f} MW | RMSE={np.mean(rmses):.2f} MW")

    # 5) Train final model on full dataset
    model.fit(X, y)

    # 6) Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nSaved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
