import os
import streamlit as st

api_key = os.getenv("FINNHUB_API_KEY")

if not api_key:
    st.warning("No se detectó la llave API. Esta app solo funciona correctamente en Streamlit Cloud.")
    # Puedes hacer st.stop() o cargar modo demo, según quieras.
