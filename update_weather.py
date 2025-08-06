# update_weather.py
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
    
def score_bee_activity(row):
    score = 0

    # Temperature
    if pd.notnull(row['TMAX_C']):
        if 20 <= row['TMAX_C'] <= 30:
            score += 0.5
        elif 15 <= row['TMAX_C'] < 20 or 30 < row['TMAX_C'] <= 35:
            score += 0.25

    # Wind
    if pd.notnull(row['WIND_m_s']):
        if row['WIND_m_s'] < 2.5:
            score += 0.2
        elif row['WIND_m_s'] < 3.5:
            score += 0.1

    # Precipitation — reduce weight since sunshine_duration added
    if pd.notnull(row['PRCP_mm']):
        if row['PRCP_mm'] == 0:
            score += 0.1
        elif 0 < row['PRCP_mm'] <= 1:
            score += 0.05

    # Sunshine (in minutes)
    if pd.notnull(row['SUN_min']):
        if row['SUN_min'] >= 480:
            score += 0.2
        elif row['SUN_min'] >= 240:
            score += 0.1

    return score

def classify_bee_activity(row):
    score = score_bee_activity(row)
    if score >= 0.75:
        return "Optimal"
    elif score >= 0.4:
        return "Moderate"
    else:
        return "Poor"


# --- Dates ---
today = datetime.today().date()
start_hist = today - timedelta(days=7)
end_hist = today - timedelta(days=1)

# --- History ---
hist_url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude=43.316&longitude=-90.850"
    f"&start_date={start_hist}&end_date={end_hist}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,sunshine_duration"
    "&temperature_unit=celsius&windspeed_unit=ms&precipitation_unit=mm&timezone=auto"
)
hist_resp = requests.get(hist_url).json()
df_hist = pd.DataFrame(hist_resp['daily'])
df_hist['date'] = pd.to_datetime(df_hist['time'])
df_hist = df_hist.drop(columns='time').rename(columns={
    'temperature_2m_max': 'TMAX_C',
    'temperature_2m_min': 'TMIN_C',
    'precipitation_sum': 'PRCP_mm',
    'windspeed_10m_max': 'WIND_m_s',
    'sunshine_duration': 'SUN_sec'
})
df_hist['SUN_min'] = df_hist['SUN_sec'] / 60
df_hist['Bee_Activity'] = df_hist.apply(classify_bee_activity, axis=1)

hist_path = 'data/bee_history.csv'
if os.path.exists(hist_path):
    old = pd.read_csv(hist_path, parse_dates=['date'])
    # Remove old rows for the updated days, then append new data
    old = old[~old['date'].isin(df_hist['date'])]
    df_hist = pd.concat([old, df_hist], ignore_index=True).sort_values('date')

df_hist.to_csv(hist_path, index=False)

# --- Forecast ---
forecast_url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.316&longitude=-90.850"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,sunshine_duration"
    "&temperature_unit=celsius&windspeed_unit=ms&precipitation_unit=mm&timezone=auto"
)
forecast_resp = requests.get(forecast_url).json()
df_forecast = pd.DataFrame(forecast_resp['daily'])
df_forecast['date'] = pd.to_datetime(df_forecast['time'])
df_forecast = df_forecast.drop(columns='time').rename(columns={
    'temperature_2m_max': 'TMAX_C',
    'temperature_2m_min': 'TMIN_C',
    'precipitation_sum': 'PRCP_mm',
    'windspeed_10m_max': 'WIND_m_s',
    'sunshine_duration': 'SUN_sec'
})
df_forecast['SUN_min'] = df_forecast['SUN_sec'] / 60
df_forecast['Bee_Activity'] = df_forecast.apply(classify_bee_activity, axis=1)
df_forecast.to_csv('data/bee_forecast.csv', index=False)
