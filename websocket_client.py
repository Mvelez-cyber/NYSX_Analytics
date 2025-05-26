import websocket
import json
import threading
from config import API_KEY

def start_websocket_thread(symbol, placeholder):
    def on_message(ws, message):
        data = json.loads(message)
        if "data" in data:
            price = data["data"][0].get("p", "N/A")
            placeholder.metric(label=f"Último Precio: {symbol}", value=f"${price:.2f}")

    def on_error(ws, error): pass
    def on_close(ws): pass
    def on_open(ws):
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    def run():
        ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={API_KEY}",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
