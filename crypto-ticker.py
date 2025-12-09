import websocket
from websocket import WebSocketApp
import json


WS_URL = "wss://advanced-trade-ws.coinbase.com"

def on_open(ws):
    subscribe_message = {
        "type": "subscribe",
        "product_ids": ["BTC-USD"],
        "channel": "ticker"
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to BTC-USD ticker channel")

def on_message(ws, message):
    data = json.loads(message)
    if data.get("channel") == "ticker":
        events = data.get("events", [])
        for event in events:
            tickers = event.get("tickers", [])
            for ticker in tickers:
                product_id = ticker.get("product_id")
                price = ticker.get("price")
                print(f"Current {product_id} price: {price}")


def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")

ws = websocket.WebSocketApp(
    WS_URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()

