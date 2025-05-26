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
                
                # Organizar la vista: datos a la izquierda, velas a la derecha
                col1, col2 = st.columns([1,2])
                with col1:
                    st.markdown("""
                    <div style='background-color:#18191A; padding: 20px; border-radius: 10px;'>
                    <h3 style='color:white;'>Datos de la Empresa</h3>
                    <p style='color:white;'><b>Precio Actual:</b> ${:.2f} <span style='color:{};'>{}</span></p>
                    <p style='color:white;'><b>Capitalización:</b> ${:.2f}B</p>
                    <p style='color:white;'><b>Volumen:</b> {:,}</p>
                    <p style='color:white;'><b>Sector:</b> {}</p>
                    </div>
                    """.format(
                        info.get('currentPrice', 0),
                        'red' if info.get('regularMarketChangePercent', 0) < 0 else 'lightgreen',
                        f"{info.get('regularMarketChangePercent', 0):.2f}%",
                        info.get('marketCap', 0)/1e9,
                        int(info.get('regularMarketVolume', 0)),
                        info.get('sector', 'N/A')
                    ), unsafe_allow_html=True)
                with col2:
                    df = get_historical_data(symbol)
                    st.plotly_chart(plot_candlestick(df), use_container_width=True)

                # Gráfico de predicción al final, ocupando todo el ancho
                st.markdown("---")
                model = train_sarimax_model(df['close'])
                forecast = forecast_with_confidence(model)
                st.plotly_chart(plot_forecast_with_confidence(df['close'], *forecast), use_container_width=True)

            except Exception as e:
                st.error(f"Error al obtener datos: {e}")
                st.info("""
                Si el error persiste, intenta:
                1. Verificar que el símbolo sea correcto
                2. Esperar unos minutos y volver a intentar
                3. Probar con otra empresa
                """)
