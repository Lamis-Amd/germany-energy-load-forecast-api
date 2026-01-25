# api/schemas.py
from pydantic import BaseModel
from typing import List

class ForecastPoint(BaseModel):
    timestamp: str
    load_mw_pred: float

class ForecastResponse(BaseModel):
    country: str = "DE"
    horizon_hours: int
    forecast: List[ForecastPoint]
