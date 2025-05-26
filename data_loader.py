import finnhub
import pandas as pd
from config import API_KEY
import requests

finnhub_client = finnhub.Client(api_key=API_KEY)

def search_company(name):
    try:
        result = finnhub_client.symbol_lookup(name)
        return result.get("result", [])
    except Exception:
        return []

def get_historical_data(symbol):
    res = finnhub_client.stock_candles(symbol, 'D', 1617753600, 1704067200)
    df = pd.DataFrame(res)
    df['t'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('t', inplace=True)
    df.rename(columns={'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open'}, inplace=True)
    return df[['open', 'high', 'low', 'close']]
