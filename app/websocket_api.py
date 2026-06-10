from fastapi import WebSocket
from game_state import GameState

class WebSocketHandler:
    """Handles WebSocket connections and commands"""
    
    def __init__(self, game_state: GameState, token: str):
        self.game_state = game_state
        self.token = token
        self.clients = set()
    
    async def accept_connection(self, websocket: WebSocket) -> bool:
        """Authenticate and accept connection"""
        token = websocket.query_params.get("token")
        if token != self.token:
            await websocket.close(code=1008)
            return False
        
        await websocket.accept()
        self.clients.add(websocket)
        return True
    
    async def broadcast_state(self) -> None:
        """Send game state to all connected clients"""
        state_json = self.game_state.to_dict()
        
        for ws in self.clients:
            try:
                await ws.send_json(state_json)
            except:
                self.clients.discard(ws)
    
    async def handle_client(self, websocket: WebSocket) -> None:
        """Handle messages from a client"""
        try:
            while True:
                data = await websocket.receive_json()
                self.process_command(data)
        finally:
            self.clients.discard(websocket)
    
    def process_command(self, data: dict) -> None:
        """Process game commands from client"""
        command_type = data.get("type")
        
        if command_type == "move_ship":
            ship_id = data.get("ship_id")
            vx = data.get("vx")
            vy = data.get("vy")
            
            if ship_id in self.game_state.ships:
                self.game_state.ships[ship_id].vx = vx
                self.game_state.ships[ship_id].vy = vy