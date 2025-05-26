from config import API_KEY
import requests
import pandas as pd
from config import API_KEY
from datetime import datetime, timedelta

def get_stock_data(symbol, days=180):
    end = int(datetime.now().timestamp())
    start = int((datetime.now() - timedelta(days=days)).timestamp())

    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        'symbol': symbol.upper(),
        'resolution': 'D',
        'from': start,
        'to': end,
        'token': API_KEY
    }

    response = requests.get(url, params=params).json()

    if response.get('s') != 'ok':
        raise ValueError("Error al obtener datos de Finnhub")

    df = pd.DataFrame({
        'timestamp': pd.to_datetime(response['t'], unit='s'),
        'open': response['o'],
        'high': response['h'],
        'low': response['l'],
        'close': response['c'],
        'volume': response['v']
    })
    df.set_index('timestamp', inplace=True)
    return df
