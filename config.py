import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")

if API_KEY is None:
    raise ValueError("La variable FINNHUB_API_KEY no está configurada.")
