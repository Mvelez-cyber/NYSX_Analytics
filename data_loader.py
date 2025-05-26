import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def search_company(name):
    try:
        # Buscar usando yfinance
        tickers = yf.Tickers(name)
        results = []
        
        # Obtener información de cada ticker encontrado
        for ticker in tickers.tickers:
            try:
                info = tickers.tickers[ticker].info
                if info and 'longName' in info:
                    results.append({
                        'symbol': ticker,
                        'description': info['longName'],
                        'exchange': info.get('exchange', 'N/A'),
                        'sector': info.get('sector', 'N/A')
                    })
            except:
                continue
                
        return results
    except Exception as e:
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
        
        # Filtrar solo días laborables (lunes a viernes)
        df = df[df.index.dayofweek < 5]  # 0-4 son lunes a viernes
        
        return df[['open', 'high', 'low', 'close']]
    except Exception as e:
        raise Exception(f"Error al obtener datos: {str(e)}")
