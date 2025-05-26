from data_loader import get_stock_data
from model import train_sarimax_model
import joblib
import os

def update_model(symbol, days=180, model_dir='models'):
    df = get_stock_data(symbol, days)
    model = train_sarimax_model(df['close'])
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, f"{model_dir}/{symbol}_sarimax.pkl")
    return f"Modelo para {symbol} actualizado."

if __name__ == "__main__":
    print(update_model("TSLA"))
