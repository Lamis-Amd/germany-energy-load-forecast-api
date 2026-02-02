# Data Documentation – Germany Electricity Load (OPSD)

This document explains the data used in the **Germany Energy Load Forecast API**, including its source, structure, meaning, and exploratory data analysis (EDA).

---

## Data Source

- **Provider:** Open Power System Data (OPSD)
- **Dataset:** Time Series – Germany Actual Load
- **Link:** https://data.open-power-system-data.org/time_series/
- **Resolution:** Hourly
- **Unit:** Megawatts (MW)

The dataset represents the **total electricity demand of Germany**, aggregated at national level.

---

## Data Structure

The data is loaded dynamically and stored in a pandas DataFrame.

### Index
- **Type:** `DatetimeIndex`
- **Timezone:** UTC
- **Frequency:** Hourly

Each index value represents a specific hour in time.

### Columns

| Column Name | Description |
|-------------|-------------|
| `load_mw` | Total electricity demand in Germany (MW) |

**Example row:**
```text
2020-10-01 18:00:00+00:00 → 62,500 MW
```

**Meaning:**  
At 6 PM UTC on October 1st, Germany consumed approximately 62.5 GW of electricity.

---

## Basic Data Inspection

Key properties of the dataset:
- Continuous numerical time series
- No categorical variables
- Strong temporal dependencies
- Clear daily and weekly cycles

This makes the dataset well suited for time-series forecasting.

---

## Exploratory Data Analysis (EDA)

### 1️⃣ Electricity Load Over Time

This plot shows the electricity demand over the last 30 days.

**Insight:**
- Clear daily cycles
- Repeating consumption patterns
- Peaks during daytime and early evening

### 2️⃣ Average Load by Hour of Day

This visualization shows the average electricity demand for each hour of the day.

**Insight:**
- Lowest demand during night hours
- Morning and evening demand peaks
- Hour of day is a strong predictor for forecasting

### 3️⃣ Weekly Consumption Patterns

Electricity demand differs between weekdays and weekends due to industrial and commercial activity.

**Insight:**
- Lower demand on weekends
- Human behavior strongly influences load patterns

---

## Why This Data Matters

Understanding electricity load patterns is critical for:
- Power grid stability
- Energy generation planning
- Integration of renewable energy
- Preventing overproduction and blackouts

This dataset reflects real-world energy system behavior, not simulated or synthetic data.

---

## Relation to the Forecasting Model

The observed patterns directly motivate:
- Lag features (1h, 24h, 168h)
- Hour-of-day features
- Day-of-week features

The machine learning model learns these patterns directly from historical data.

---

## Summary

- Real national-level energy data
- Hourly time-series structure
- Strong temporal and behavioral patterns
- Direct relevance to energy digitalization and climate-tech
