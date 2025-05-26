# data_loader.py
import requests
import pandas as pd
from config import FINNHUB_API_KEY
from datetime import datetime, timedelta

def get_stock_data(symbol, resolution='D', days=365):
    end = int(datetime.now().timestamp())
    start = int((datetime.now() - timedelta(days=days)).timestamp())

    url = f"https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": start,
        "to": end,
        "token": FINNHUB_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['s'] != 'ok':
        raise Exception("Error fetching data from Finnhub API")

    df = pd.DataFrame({
        'time': pd.to_datetime(data['t'], unit='s'),
        'open': data['o'],
        'high': data['h'],
        'low': data['l'],
        'close': data['c'],
        'volume': data['v']
    })

    return df.set_index('time')
