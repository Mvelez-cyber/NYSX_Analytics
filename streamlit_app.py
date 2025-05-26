import streamlit as st
from data_loader import search_company, get_historical_data
from model import train_sarimax_model, forecast_with_confidence
from visualization import plot_candlestick, plot_forecast_with_confidence
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="NYSE Stock Forecast Dashboard", layout="wide")
st.title("📈 NYSE Stock Forecast Dashboard")

# Advertencia sobre predicciones
st.info("""
ℹ️ **Nota Importante**: 
Los datos históricos mostrados son reales y provienen de Yahoo Finance.
Las predicciones se basan en modelos estadísticos y deben tomarse como referencia únicamente.
""")

# Buscar empresa
company_name = st.text_input("🔍 Ingresa el nombre de la empresa o símbolo (ej: Apple, AAPL, Microsoft, MSFT):", "")

if company_name:
    with st.spinner('Buscando empresas...'):
        matches = search_company(company_name)

    if not matches:
        st.error("""
        No se encontraron empresas. Por favor:
        1. Verifica que el nombre o símbolo sea correcto
        2. Intenta con otro nombre o símbolo
        3. Asegúrate de que la empresa esté listada en NYSE o NASDAQ
        """)
    else:
        # Crear un selector con información detallada
        options = [f"{m['symbol']} - {m['description']} ({m['exchange']})" for m in matches]
        selected_option = st.selectbox(
            "Selecciona la empresa:",
            options,
            format_func=lambda x: x
        )
        
        if selected_option:
            # Extraer el símbolo de la opción seleccionada
            symbol = selected_option.split(' - ')[0]
            
            try:
                # Obtener información detallada de la empresa
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                if not info:
                    raise Exception("No se pudo obtener información de la empresa")
                
                # Mostrar información de la empresa en columnas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Precio Actual",
                        f"${info.get('currentPrice', 'N/A'):.2f}",
                        f"{info.get('regularMarketChangePercent', 0):.2f}%"
                    )
                
                with col2:
                    st.metric(
                        "Capitalización",
                        f"${info.get('marketCap', 0)/1e9:.2f}B"
                    )
                
                with col3:
                    st.metric(
                        "Volumen",
                        f"{info.get('regularMarketVolume', 0):,}"
                    )
                
                with col4:
                    st.metric(
                        "Sector",
                        info.get('sector', 'N/A')
                    )
                
                # Mostrar datos históricos
                df = get_historical_data(symbol)
                st.plotly_chart(plot_candlestick(df), use_container_width=True)

                # Entrenar modelo y predecir
                model = train_sarimax_model(df['close'])
                forecast = forecast_with_confidence(model)
                st.plotly_chart(plot_forecast_with_confidence(df['close'], *forecast), use_container_width=True)

            except Exception as e:
                st.error(f"Error al obtener datos: {str(e)}")
                st.info("""
                Si el error persiste, intenta:
                1. Verificar que el símbolo sea correcto
                2. Esperar unos minutos y volver a intentar
                3. Probar con otra empresa
                """)
