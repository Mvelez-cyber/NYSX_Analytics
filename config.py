import os
import streamlit as st

API_KEY = st.secrets["FINNHUB_API_KEY"]

if not API_KEY:
    st.warning("No se detectó la llave API. Esta app solo funciona correctamente en Streamlit Cloud.")
    # Puedes hacer st.stop() o cargar modo demo, según quieras.
