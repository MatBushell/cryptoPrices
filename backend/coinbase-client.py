import websockets
import asyncio
import json


# Coinbase url
WS_URL = "wss://ws-feed.exchange.coinbase.com"


product_ids = ["BTC-USD"]
subscribe_message = {
    'type': 'subscribe',
    'product_ids': product_ids,
    'channels': ['ticker'],
}

# Def the listener function
async def websocket_listener(on_ticker_update):
    message = json.dumps(subscribe_message)

    while True:
        try:
            async with websockets.connect(WS_URL, ping_interval=None) as websocket:
                await websocket.send(message)
                while True:
                    response = await websocket.recv()
                    data = json.loads(response)
                    if data.get("type") == "ticker":
                        await on_ticker_update(data) # call the callback

        
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
            print('Connection closed, retrying..')
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(websocket_listener())
    except KeyboardInterrupt:
        print("Exiting WebSocket..")


