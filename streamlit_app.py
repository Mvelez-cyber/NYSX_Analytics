import streamlit as st
from data_loader import search_company, get_historical_data
from model import train_sarimax_model, forecast_with_confidence
from visualization import plot_candlestick, plot_forecast_with_confidence
from websocket_client import start_websocket_thread
import pandas as pd

st.set_page_config(page_title="NYSE Stock Forecast Dashboard", layout="wide")
st.title("📈 NYSE Stock Forecast Dashboard")

# Buscar empresa
company_name = st.text_input("🔍 Busca una acción del NYSE:", "")

if company_name:
    matches = search_company(company_name)

    if not matches:
        st.error("No se encontraron empresas.")
    else:
        symbol = st.selectbox("Selecciona el símbolo de la empresa:", [m['symbol'] for m in matches])
        
        if symbol:
            try:
                # Mostrar datos históricos
                df = get_historical_data(symbol)
                st.plotly_chart(plot_candlestick(df), use_container_width=True)

                # Entrenar modelo y predecir
                model = train_sarimax_model(df['close'])
                forecast = forecast_with_confidence(model)
                st.plotly_chart(plot_forecast_with_confidence(df['close'], *forecast), use_container_width=True)

                # Iniciar WebSocket (muestra en tiempo real debajo)
                st.subheader("📡 Precio en tiempo real:")
                real_time_price = st.empty()
                start_websocket_thread(symbol, real_time_price)

            except Exception as e:
                st.error(f"Error al obtener datos: {e}")
