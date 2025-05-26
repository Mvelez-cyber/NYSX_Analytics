import streamlit as st
import finnhub
import pandas as pd
from data_loader import get_stock_data
from visualization import plot_candlestick
import os

# Cargar clave API desde variables de entorno
finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

st.set_page_config(page_title="NYSE Stock Forecast Dashboard", layout="wide")
st.title("📈 NYSE Stock Forecast Dashboard")

# Paso 1: Buscar nombre de empresa
company_name = st.text_input("🔎 Busca una empresa del NYSE:")

if company_name:
    lookup_result = finnhub_client.symbol_lookup(company_name)
    matches = lookup_result.get("result", [])

    if not matches:
        st.error("❌ No se encontraron coincidencias.")
    else:
        # Paso 2: Seleccionar el símbolo
        symbol_options = {f"{m['description']} ({m['symbol']})": m["symbol"] for m in matches}
        selected_description = st.selectbox("Selecciona una acción:", list(symbol_options.keys()))
        selected_symbol = symbol_options[selected_description]

        # Paso 3: Obtener y mostrar datos
        try:
            df = get_stock_data(selected_symbol)
            st.subheader(f"📊 Historial para {selected_symbol}")
            st.plotly_chart(plot_candlestick(df), use_container_width=True)

            # Paso 4: Último precio (Last Trade)
            quote = finnhub_client.quote(selected_symbol)
            current_price = quote["c"]
            st.metric(label="💵 Último Precio", value=f"${current_price:.2f}")

        except Exception as e:
            st.error(f"Error al obtener datos: {e}")
