import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import finnhub
from config import API_KEY

# Inicializar cliente de Finnhub solo para búsqueda
finnhub_client = finnhub.Client(api_key=API_KEY)

def search_company(name):
    try:
        # Usar Finnhub para la búsqueda de símbolos
        results = finnhub_client.symbol_lookup(name)
        
        if not results or 'result' not in results:
            return []
            
        # Filtrar solo resultados de NYSE y NASDAQ
        filtered_results = []
        for item in results['result']:
            if item.get('type') == 'Common Stock' and item.get('primaryExchange') in ['NYQ', 'NMS']:
                filtered_results.append({
                    'symbol': item['symbol'],
                    'description': item['description'],
                    'exchange': 'NYSE' if item.get('primaryExchange') == 'NYQ' else 'NASDAQ',
                    'type': item.get('type', 'N/A')
                })
        
        return filtered_results
    except Exception as e:
        return []

def get_historical_data(symbol):
    try:
        # Obtener datos históricos de los últimos 30 días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Descargar datos históricos usando yfinance
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        
        # Renombrar columnas para mantener consistencia
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close'
        })
        
        # Filtrar solo días laborables (lunes a viernes)
        df = df[df.index.dayofweek < 5]  # 0-4 son lunes a viernes
        
        return df[['open', 'high', 'low', 'close']]
    except Exception as e:
        raise Exception(f"Error al obtener datos: {str(e)}")
