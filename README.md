# OPSD Germany Load Forecast – Dockerized ML API

## Overview
This project is a **Dockerized machine learning service** that forecasts **Germany’s hourly electricity load** using real historical data from **Open Power System Data (OPSD)**.

The system demonstrates how **energy engineering domain knowledge** can be combined with **data-driven modeling** and **modern MLOps practices** to build production-ready energy analytics services.

---

## Project Motivation
Energy systems generate large amounts of time-series data. Even **simple, well-designed machine learning models** can provide valuable insights for:

- Load forecasting  
- Operational planning  
- System monitoring  
- Energy optimization  

This project aims to show a **practical, industry-oriented approach** rather than academic overengineering.

---

## Data Source
- **Dataset:** Open Power System Data – Time Series  
- **Country:** Germany (DE)  
- **Resolution:** Hourly  
- **Target:** Actual electricity load (MW)  

**Attribution:**  
Open Power System Data. *Data Package Time series*  
Version: 2020-10-06  
DOI: https://doi.org/10.25832/time_series/2020-10-06

---

## Technical Stack
- Python 3.11  
- pandas / NumPy – data processing  
- scikit-learn – time-series regression (Ridge)  
- FastAPI – REST API  
- Uvicorn – ASGI server  
- Docker – containerization  

---

## System Architecture

Real OPSD Data
↓
Feature Engineering
(time lags, rolling stats)
↓
ML Model (Ridge Regression)
↓
FastAPI Service
↓
Docker Container

---

## Machine Learning Approach
- **Problem type:** Time-series regression  
- **Features:**
  - Hour of day  
  - Day of week  
  - Lagged load values (1h, 24h, 168h)  
  - Rolling mean & standard deviation (24h)  
- **Model:** Ridge Regression  
- **Validation:** TimeSeriesSplit cross-validation  
- **Output:** Next-hour iterative forecast (up to 72h)  

The focus is on **robust baselines**, **interpretability**, and **operational suitability**.

---

## API Endpoints

### Health Check

GET /health
Response:
```json
{ "status": "ok" }

Load Forecast
GET /forecast?horizon_hours=24
Response:
{
  "country": "DE",
  "horizon_hours": 24,
  "forecast": [
    {
      "timestamp": "2020-10-01T00:00:00+00:00",
      "load_mw_pred": 43727.4
    }
  ]
}
API Documentation
GET /docs

Swagger UI with full OpenAPI schema.
____________________________________________________________________________________________________
Running the Project
1️⃣ Build Docker Image
docker build -t opsd-load-forecast .

2️⃣ Run Container
docker run -p 8000:8000 opsd-load-forecast

3️⃣ Open in Browser

http://127.0.0.1:8000/health

http://127.0.0.1:8000/forecast?horizon_hours=24

http://127.0.0.1:8000/docs

Project Structure
opsd-de-load-forecast/
├─ api/
│  ├─ main.py
│  └─ schemas.py
├─ src/
│  ├─ data.py
│  ├─ features.py
│  ├─ train.py
│  └─ anomaly.py
├─ models/
│  └─ model.joblib
├─ Dockerfile
├─ requirements.txt
└─ README.md

Why This Project Matters

Uses real German energy data

Applies engineering-aware feature design

Follows production-ready patterns

Demonstrates end-to-end ML lifecycle

Directly relevant to energy digitalization, climate-tech, and Industry 4.0

Author

Lamis Ahmad
Background in Electrical & Mechatronics Engineering with a Master’s focus in Artificial Intelligence.
Interested in energy systems, data-driven modeling, and industrial AI applications.

Open to junior full-time roles or Praktikum opportunities in Germany.

License

This project is for educational and demonstration purposes.
Data usage follows the OPSD license and attribution requirements.


---
