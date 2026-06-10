from typing import Dict
from models import Ship, Station

class GameState:
    """Central game state - shared by all systems"""
    
    def __init__(self):
        self.ships: Dict[int, Ship] = {}
        self.stations: Dict[int, Station] = {}
        self.resources: Dict[str, int] = {}
    
    def add_ship(self, ship: Ship) -> None:
        self.ships[ship.id] = ship
    
    def update_ship_position(self, ship_id: int, x: float, y: float) -> None:
        if ship_id in self.ships:
            self.ships[ship_id].x = x
            self.ships[ship_id].y = y
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            "ships": {id: self._ship_to_dict(ship) for id, ship in self.ships.items()},
            "stations": {id: self._station_to_dict(st) for id, st in self.stations.items()},
        }
    
    @staticmethod
    def _ship_to_dict(ship: Ship) -> dict:
        return {
            "id": ship.id,
            "name": ship.name,
            "x": ship.x,
            "y": ship.y,
            "vx": ship.vx,
            "vy": ship.vy,
        }
    
    @staticmethod
    def _station_to_dict(station: Station) -> dict:
        return {
            "id": station.id,
            "name": station.name,
            "x": station.x,
            "y": station.y,
            "resources": station.resources,
        }