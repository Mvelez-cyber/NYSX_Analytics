import streamlit as st
from data_loader import search_company, get_historical_data
from model import train_sarimax_model, forecast_with_confidence
from visualization import plot_candlestick, plot_forecast_with_confidence
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="NYSE Stock Forecast Dashboard", layout="wide")
st.title("📈 NYSE Stock Forecast Dashboard")

# Advertencia sobre datos simulados
st.warning("""
⚠️ **Nota Importante**: 
Los datos históricos mostrados son simulados debido a limitaciones de la API gratuita.
Las predicciones se basan en estos datos simulados y deben tomarse como referencia únicamente.
""")

# Buscar empresa
company_name = st.text_input("🔍 Ingresa el símbolo de la acción (ej: AAPL, MSFT, GOOGL):", "")

if company_name:
    matches = search_company(company_name)

    if not matches:
        st.error("No se encontró la acción. Verifica el símbolo e intenta de nuevo.")
    else:
        symbol = matches[0]['symbol']
        
        try:
            # Mostrar datos históricos
            df = get_historical_data(symbol)
            
            # Mostrar información básica de la empresa
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Precio Actual", f"${info.get('currentPrice', 'N/A'):.2f}")
            with col2:
                st.metric("Cambio %", f"{info.get('regularMarketChangePercent', 'N/A'):.2f}%")
            with col3:
                st.metric("Volumen", f"{info.get('regularMarketVolume', 'N/A'):,}")
            
            # Gráfico de velas
            st.plotly_chart(plot_candlestick(df), use_container_width=True)

            # Entrenar modelo y predecir
            model = train_sarimax_model(df['close'])
            forecast = forecast_with_confidence(model)
            st.plotly_chart(plot_forecast_with_confidence(df['close'], *forecast), use_container_width=True)

        except Exception as e:
            st.error(f"Error al obtener datos: {e}")
