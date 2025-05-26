from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
import os

def train_sarimax_model(series, order=(1,1,1), seasonal_order=(1,1,1,12)):
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    results = model.fit(disp=False)
    return results

def load_model(symbol, model_dir='models'):
    path = f"{model_dir}/{symbol}_sarimax.pkl"
    return joblib.load(path) if os.path.exists(path) else None

def forecast_with_confidence(model, steps=30):
    forecast = model.get_forecast(steps=steps)
    return forecast.predicted_mean, forecast.conf_int()
