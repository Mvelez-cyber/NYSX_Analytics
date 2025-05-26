import streamlit as st
from data_loader import get_stock_data
from model import load_model, train_sarimax_model, forecast_with_confidence
from visualization import plot_candlestick, plot_forecast_with_confidence

st.set_page_config(layout="wide", page_title="NYSE Stock Forecast")

st.title("📈 NYSE Stock Forecast Dashboard")

symbol = st.text_input("🔍 Busca una acción del NYSE:", "TSLA").upper()

try:
    df = get_stock_data(symbol)
    st.plotly_chart(plot_candlestick(df), use_container_width=True)

    model = load_model(symbol)
    if not model:
        st.warning("Modelo no encontrado. Entrenando...")
        model = train_sarimax_model(df['close'])

    forecast, conf = forecast_with_confidence(model)
    st.plotly_chart(plot_forecast_with_confidence(df['close'], forecast, conf), use_container_width=True)

except Exception as e:
    st.error(f"❌ Error: {e}")
