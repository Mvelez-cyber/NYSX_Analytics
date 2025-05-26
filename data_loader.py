import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def search_company(name):
    try:
        # yfinance no tiene una función de búsqueda directa, así que usamos Ticker
        ticker = yf.Ticker(name)
        info = ticker.info
        return [{'symbol': name, 'description': info.get('longName', name)}]
    except Exception:
        return []

def get_historical_data(symbol):
    try:
        # Obtener datos históricos de los últimos 30 días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Descargar datos históricos
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        # Renombrar columnas para mantener consistencia
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close'
        })
        
        return df[['open', 'high', 'low', 'close']]
    except Exception as e:
        raise Exception(f"Error al obtener datos: {str(e)}")
