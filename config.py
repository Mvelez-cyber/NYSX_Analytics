import os
import streamlit as st

# Intentar obtener la API key de diferentes fuentes
API_KEY = os.getenv('FINNHUB_API_KEY') or st.secrets.get("FINNHUB_API_KEY")

if not API_KEY:
    st.warning("No se detectó la llave API de Finnhub. La búsqueda de empresas no funcionará correctamente.")
    # Puedes hacer st.stop() o cargar modo demo, según quieras.
