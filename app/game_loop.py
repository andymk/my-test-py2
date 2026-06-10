import asyncio
from game_state import GameState

class GameSimulation:
    """Handles game loop and ship updates"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    async def run(self) -> None:
        """Main game loop (10 Hz)"""
        while True:
            self.update_ships(dt=0.1)
            self.check_mining()
            self.process_trades()
            
            await asyncio.sleep(0.1)
    
    def update_ships(self, dt: float) -> None:
        """Update all ship positions"""
        for ship in self.game_state.ships.values():
            ship.update(dt)
    
    def check_mining(self) -> None:
        """Check if ships are mining resources"""
        for ship in self.game_state.ships.values():
            # Mining logic here
            pass
    
    def process_trades(self) -> None:
        """Process trade orders"""
        # Trade logic here
        pass