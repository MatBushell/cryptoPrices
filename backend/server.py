from fastapi import FastAPI, WebSocket, WebSocketDisconnect 
from fastapi.middleware.cors import CORSMiddleware
from coinbase_client import websocket_listener
from contextlib import asynccontextmanager
import asyncio


# Store active clients
active_clients = set()

# Pass data to all clients in active_clients
async def broadcast_to_clients(data: dict):
    payload = {
    "product_id": data.get("product_id"),
    "price": data.get("price"),
    }
    for client in list(active_clients):
        try:
            await client.send_json(payload)
        except Exception:
            active_clients.discard(client)


# Use lifespan(FastAPI) to start the listener once upon startup and handle shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the listener
    task = asyncio.create_task(websocket_listener(broadcast_to_clients))
    yield
    # cleanup
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass



# Initialize Fast API
app = FastAPI(lifespan=lifespan)

# CORS setup
# Allowed origins
origins = [
    "http://localhost:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Endpoint
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text() # kepp connection open
    except WebSocketDisconnect:
        pass
    finally:
        active_clients.discard(websocket)




