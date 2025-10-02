# backend/schemas/api_schemas.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict
from .common_schemas import Drone, Asset, VisualEvent, Position # Import Position

class CoordinationTarget(BaseModel):
    source_id: str
    target_id: str
    distance: int

class SwarmStateSummary(BaseModel):
    status: str
    count: int

class AnalysisData(BaseModel):
    coordination_targets: List[CoordinationTarget] = []
    swarm_state: List[SwarmStateSummary] = []

class SimulationState(BaseModel):
    status: Literal['idle', 'running', 'paused', 'finished']
    time: float

# --- THIS IS A CRITICAL FIX FOR ANIMATIONS ---
# We add an optional target_position to the event
class VisualEventWithTarget(VisualEvent):
    target_position: Optional[Position] = None

class SimulationStreamData(BaseModel):
    simulation_state: Dict
    drones: List[Dict]
    assets: List[Dict]
    visual_events: List[Dict]
    metrics: Dict
    event_log: List[Dict]
    analysis: AnalysisData
    
class Command(BaseModel):
    command: Literal["start", "pause", "resume", "reset"]
    scenario_id: Optional[str] = None
    num_friendly: Optional[int] = None
    num_enemy: Optional[int] = None

class ScenarioInfo(BaseModel):
    id: str
    name: str