import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from game_state import GameState

Base = declarative_base()

class GameSnapshot(Base):
    __tablename__ = "game_snapshots"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    state_json = Column(String)

class Database:
    """Handle database operations"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    
    def save_game_state(self, game_state: GameState) -> None:
        """Save game state to database"""
        session = self.Session()
        try:
            snapshot = GameSnapshot(state_json=json.dumps(game_state.to_dict()))
            session.add(snapshot)
            session.commit()
            print(f"✓ Saved game state")
        except Exception as e:
            print(f"✗ Save failed: {e}")
            session.rollback()
        finally:
            session.close()
    
    def load_latest_game_state(self) -> GameState:
        """Load latest game state from database"""
        session = self.Session()
        try:
            latest = session.query(GameSnapshot).order_by(GameSnapshot.timestamp.desc()).first()
            
            if latest:
                state_dict = json.loads(latest.state_json)
                # Reconstruct GameState from dict
                return self._dict_to_game_state(state_dict)
            else:
                return GameState()  # Empty state
        finally:
            session.close()
    
    @staticmethod
    def _dict_to_game_state(state_dict: dict) -> GameState:
        """Convert dict back to GameState"""
        from models import Ship, Station
        
        game_state = GameState()
        
        for ship_id, ship_data in state_dict.get("ships", {}).items():
            ship = Ship(
                id=ship_data["id"],
                name=ship_data["name"],
                x=ship_data["x"],
                y=ship_data["y"],
                vx=ship_data["vx"],
                vy=ship_data["vy"],
            )
            game_state.add_ship(ship)
        
        return game_state