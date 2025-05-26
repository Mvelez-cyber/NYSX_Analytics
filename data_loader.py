from config import API_KEY
import requests
import pandas as pd
from config import API_KEY
from datetime import datetime, timedelta
import finnhub
import os

finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))

def get_stock_data(symbol):
    now = int(datetime.now().timestamp())
    last_year = int((datetime.now() - timedelta(days=365)).timestamp())
    res = finnhub_client.stock_candles(symbol, 'D', last_year, now)

    if res['s'] != 'ok':
        raise Exception("No se pudo obtener el historial")

    df = pd.DataFrame({
        'time': pd.to_datetime(res['t'], unit='s'),
        'open': res['o'],
        'high': res['h'],
        'low': res['l'],
        'close': res['c']
    })
    df.set_index('time', inplace=True)
    return df
