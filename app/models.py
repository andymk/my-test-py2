from dataclasses import dataclass

@dataclass
class Ship:
    id: int
    name: str
    x: float
    y: float
    vx: float
    vy: float
    
    def update(self, dt: float) -> None:
        """Update position"""
        self.x += self.vx * dt
        self.y += self.vy * dt

@dataclass
class Station:
    id: int
    name: str
    x: float
    y: float
    sector: tuple
    resources: dict