# backend/schemas/common_schemas.py
from pydantic import BaseModel, Field
from typing import Literal, Optional

class Position(BaseModel):
    x: float
    y: float

class Drone(BaseModel):
    id: str
    team: Literal['friendly', 'enemy']
    type: Literal['interceptor', 'ground_attack', 'air_to_air']
    position: Position
    velocity: Position = Field(default_factory=lambda: Position(x=0.0, y=0.0))
    status: str = Field(default='patrolling')
    health: int = Field(default=100)
    target_id: Optional[str] = None

class Asset(BaseModel):
    id: str
    position: Position
    health: int = Field(default=100)

class VisualEvent(BaseModel):
    id: str
    # --- THE FIX: Add 'comm_link' as a valid event type ---
    type: Literal['neutralization', 'weapon_fire', 'comm_link']
    # -------------------------------------------------------
    position: Position
    ttl: float
    team: Optional[str] = None # 'friendly' or 'enemy'
    target_position: Optional[Position] = None
