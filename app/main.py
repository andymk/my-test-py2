import asyncio
from fastapi import FastAPI, WebSocket
from game_state import GameState
from game_loop import GameSimulation
from websocket_api import WebSocketHandler
from database import Database
from logging_config import setup_logging

# logging
setup_logging()

# Database
db = Database("sqlite:///./game.db")

# Load game state from database, or create new
game_state = db.load_latest_game_state()

# Simulation and WebSocket handler
simulation = GameSimulation(game_state)
ws_handler = WebSocketHandler(game_state, token="my-secret-token")

app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(simulation.run())
    asyncio.create_task(broadcast_loop())
    asyncio.create_task(save_loop())  # New: periodic saves

async def broadcast_loop():
    while True:
        await ws_handler.broadcast_state()
        await asyncio.sleep(0.1)

async def save_loop():
    """Save game state every 30 seconds"""
    while True:
        await asyncio.sleep(30)
        db.save_game_state(game_state)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if await ws_handler.accept_connection(websocket):
        await ws_handler.handle_client(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)