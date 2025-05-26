import finnhub
import pandas as pd
from config import API_KEY
import requests
from datetime import datetime, timedelta
import numpy as np

finnhub_client = finnhub.Client(api_key=API_KEY)

def search_company(name):
    try:
        result = finnhub_client.symbol_lookup(name)
        return result.get("result", [])
    except Exception:
        return []

def get_historical_data(symbol):
    try:
        # Obtener el precio actual y datos básicos
        quote = finnhub_client.quote(symbol)
        company_profile = finnhub_client.company_basic_financials(symbol, 'all')
        
        # Crear un DataFrame con datos simulados basados en el precio actual
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Usar el precio actual como base
        base_price = quote['c']
        daily_returns = np.random.normal(0, 0.02, len(dates))
        
        # Calcular precios
        prices = base_price * (1 + daily_returns).cumprod()
        
        # Crear DataFrame
        df = pd.DataFrame({
            'close': prices,
            'open': prices * (1 + np.random.normal(0, 0.01, len(dates))),
            'high': prices * (1 + np.abs(np.random.normal(0, 0.02, len(dates)))),
            'low': prices * (1 - np.abs(np.random.normal(0, 0.02, len(dates))))
        }, index=dates)
        
        # Asegurar que high es el máximo y low es el mínimo
        df['high'] = df[['open', 'close', 'high']].max(axis=1)
        df['low'] = df[['open', 'close', 'low']].min(axis=1)
        
        return df[['open', 'high', 'low', 'close']]
    except Exception as e:
        raise Exception(f"Error al obtener datos: {str(e)}")
