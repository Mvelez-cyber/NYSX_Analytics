# app.py
import streamlit as st
from data_loader import get_stock_data
from model import load_model, train_sarimax_model, forecast_with_confidence
from visualization import plot_candlestick, plot_forecast_with_confidence

st.set_page_config(layout="wide", page_title="NYSE Stock Tracker and Forecast")

st.title("📈 NYSE Stock Tracker and Forecast")

# Sidebar
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "TSLA")

try:
    df = get_stock_data(symbol)
    st.subheader(f"Latest {symbol} Candlestick Chart")
    st.plotly_chart(plot_candlestick(df), use_container_width=True)

    # Load existing model or retrain if not found
    st.subheader("SARIMAX Forecast with Confidence Interval")
    model = load_model(symbol)
    if model is None:
        st.warning("Model not found. Training new one...")
        model = train_sarimax_model(df['close'])

    forecast, conf = forecast_with_confidence(model)
    st.plotly_chart(plot_forecast_with_confidence(df['close'], forecast, conf), use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
