# model.py
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
import pandas as pd
import os

def train_sarimax_model(series, order=(1,1,1), seasonal_order=(1,1,1,12)):
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    return results

def load_model(symbol, model_dir='models'):
    model_path = f"{model_dir}/{symbol}_sarimax.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

def forecast_with_confidence(model, steps=30):
    forecast = model.get_forecast(steps=steps)
    mean = forecast.predicted_mean
    conf_int = forecast.conf_int()
    return mean, conf_int
