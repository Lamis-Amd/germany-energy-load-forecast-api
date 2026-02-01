# OPSD Germany Load Forecast – Dockerized ML API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange)
![Energy Data](https://img.shields.io/badge/Energy-OPSD-yellow)



## Overview
This project is a **Dockerized machine learning service** that forecasts **Germany's hourly electricity load** using real historical data from **Open Power System Data (OPSD)**.

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
```
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
```

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
```http
GET /health
```

Response:
```json
{ "status": "ok" }
```

### Load Forecast
```http
GET /forecast?horizon_hours=24
```

Response:
```json
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
```

### API Documentation
```http
GET /docs
```
Swagger UI with full OpenAPI schema.

---

## Running the Project

### 1️⃣ Build Docker Image
```bash
docker build -t opsd-load-forecast .
```

### 2️⃣ Run Container
```bash
docker run -p 8000:8000 opsd-load-forecast
```

### 3️⃣ Open in Browser
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/forecast?horizon_hours=24
- http://127.0.0.1:8000/docs

---
### Plot Visualizations (PNG)

- **GET** `/plots/last30days`  
Returns a PNG chart of Germany’s load for the last 30 days.

- **GET** `/plots/avg-by-hour`  
Returns a PNG chart of average load by hour of day.

---

## Project Structure
```
opsd-de-load-forecast/
├─ api/
│  ├─ __init__.py
│  ├─ main.py
│  └─ schemas.py
├─ src/
│  ├─ __init__.py
│  ├─ data.py
│  ├─ features.py
│  ├─ train.py
│  ├─ anomaly.py
│  ├─ plotting.py
│  └─ visualize_data.py
├─ models/
│  └─ model.joblib
├─ figures/
│  ├─ elec_load_last30days.png
│  ├─ avg_load_per_hour.png
│  ├─ Figure_1.png
│  ├─ Figure_2.png
│  └─ Figure_3.png
├─ .gitignore
├─ Dockerfile
├─ dockerignore
├─ requirements.txt
└─ README.md
```

---

## Why This Project Matters
- Uses real German energy data
- Applies engineering-aware feature design
- Follows production-ready patterns
- Demonstrates end-to-end ML lifecycle
- Directly relevant to energy digitalization, climate-tech, and Industry 4.0

## Author

**Lamis Ahmad**
Background in Electrical & Mechatronics Engineering with a Master’s degree in Artificial Intelligence.
Interested in industrial AI applications.

---

## License
This project is for educational and demonstration purposes.

Data usage follows the OPSD license and attribution requirements.


---
