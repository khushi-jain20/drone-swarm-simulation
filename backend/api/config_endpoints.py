# api/config_endpoints.py
from fastapi import APIRouter
from pydantic import BaseModel
from core import config

class SpeedSetting(BaseModel):
    multiplier: float

class AiLevelSetting(BaseModel):
    level: str

class WorldConfig(BaseModel):
    world_width: int
    world_height: int

router = APIRouter()

@router.get("/config/world", response_model=WorldConfig)
def get_world_config():
    return {"world_width": config.WORLD_WIDTH, "world_height": config.WORLD_HEIGHT}

@router.post("/config/speed")
def set_speed(settings: SpeedSetting):
    config.SPEED_MULTIPLIER = max(0.1, settings.multiplier)
    return {"status": "success", "speed_multiplier": config.SPEED_MULTIPLIER}

# --- THIS IS THE CORRECTED AND FINAL VERSION OF THIS ENDPOINT ---
@router.post("/config/ai_level")
def set_ai_level(settings: AiLevelSetting):
    """Sets AI difficulty level and prints a confirmation to the console."""
    level = settings.level
    if level not in ("basic", "normal", "advanced", "adaptive"):
        return {"error": "invalid level"}, 400
    
    # This is the line that updates the global configuration
    config.AI_INTELLIGENCE_LEVEL = level
    
    # Added a print statement for immediate feedback in your terminal
    print(f"[CONFIG] AI Intelligence Level set to: {config.AI_INTELLIGENCE_LEVEL.upper()}")
    
    return {"status": "success", "ai_intelligence_level": config.AI_INTELLIGENCE_LEVEL}
