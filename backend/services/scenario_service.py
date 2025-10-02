# services/scenario_service.py
from typing import Dict, List
from schemas.api_schemas import ScenarioInfo
from core import config # <-- Import config
import random

# Use world dimensions from the central config file
WORLD_WIDTH = config.WORLD_WIDTH
WORLD_HEIGHT = config.WORLD_HEIGHT
SPAWN_PADDING = 100

SCENARIOS_BLUEPRINT: Dict[str, Dict] = {
    "small_swarm": {
        "id": "small_swarm",
        "name": "Small Swarm (3v2)",
        "num_friendly": 3, "num_enemy_aa": 1, "num_enemy_ga": 1, "num_assets": 1
    },
    "large_swarm_threat": {
        "id": "large_swarm_threat",
        "name": "Large Swarm (10v13)",
        "num_friendly": 10, "num_enemy_aa": 5, "num_enemy_ga": 8, "num_assets": 2
    },
    "asset_under_threat": {
        "id": "asset_under_threat",
        "name": "Asset Under Threat (6v4)",
        "num_friendly": 6, "num_enemy_aa": 0, "num_enemy_ga": 4, "num_assets": 2
    },
}

def generate_custom_scenario(num_friendly: int, num_enemy: int) -> Dict:
    """Creates a scenario dynamically based on user-defined drone counts."""
    # Clamp values to a max of 20 to prevent performance issues
    num_friendly = min(num_friendly, 20)
    num_enemy = min(num_enemy, 20)

    # Default to 2 assets for custom battles
    assets = [{"id": f"A{i+1}", "position": {
        "x": (WORLD_WIDTH / 3) * (i + 1), "y": WORLD_HEIGHT - 50
    }} for i in range(2)]

    # Spawn friendly drones in a line at the bottom
    friendly_drones = [{"id": f"F{i+1}", "team": "friendly", "type": "interceptor", "position": {
        "x": (WORLD_WIDTH / (num_friendly + 1)) * (i + 1),
        "y": WORLD_HEIGHT - SPAWN_PADDING
    }} for i in range(num_friendly)]
    
    # Spawn enemy drones randomly at the top, split between types
    enemy_drones = []
    num_ga = num_enemy // 2  # Half are ground-attack
    num_aa = num_enemy - num_ga # The rest are air-to-air
    
    for i in range(num_enemy):
        is_ga = i < num_ga
        drone_type = "ground_attack" if is_ga else "air_to_air"
        drone_id = f"E-GA{i+1}" if is_ga else f"E-AA{i - num_ga + 1}"
        
        enemy_drones.append({
            "id": drone_id, "team": "enemy", "type": drone_type,
            "position": {
                "x": random.uniform(SPAWN_PADDING, WORLD_WIDTH - SPAWN_PADDING),
                "y": random.uniform(SPAWN_PADDING, SPAWN_PADDING + 150)
            }
        })
    
    return {
        "name": f"Custom Battle ({num_friendly}v{num_enemy})",
        "friendly_drones": friendly_drones,
        "enemy_drones": enemy_drones,
        "assets": assets
    }

def get_scenario_list() -> List[ScenarioInfo]:
    return [ScenarioInfo(**{"id": sc["id"], "name": sc["name"]}) for sc in SCENARIOS_BLUEPRINT.values()]

def get_scenario(scenario_id: str) -> Dict:
    blueprint = SCENARIOS_BLUEPRINT.get(scenario_id)
    if not blueprint:
        return None
    
    # Spawn assets on the friendly side (bottom of the screen)
    assets = [{"id": f"A{i+1}", "position": {
        "x": (WORLD_WIDTH / (blueprint['num_assets'] + 1)) * (i + 1),
        "y": WORLD_HEIGHT - 50  # Positioned near the very bottom
    }} for i in range(blueprint["num_assets"])]

    # Spawn friendly drones in a line, safely inside the screen
    friendly_drones = [{"id": f"F{i+1}", "team": "friendly", "type": "interceptor", "position": {
        "x": (WORLD_WIDTH / (blueprint["num_friendly"] + 1)) * (i + 1),
        "y": WORLD_HEIGHT - SPAWN_PADDING # Spawn them away from the edge
    }} for i in range(blueprint["num_friendly"])]
    
    # Spawn enemy drones randomly at the top of the screen
    enemy_drones = []
    num_enemies = blueprint["num_enemy_aa"] + blueprint["num_enemy_ga"]
    for i in range(num_enemies):
        drone_type = "ground_attack" if i < blueprint["num_enemy_ga"] else "air_to_air"
        drone_id = f"E-GA{i+1}" if drone_type == "ground_attack" else f"E-AA{i - blueprint['num_enemy_ga']+1}"
        
        enemy_drones.append({
            "id": drone_id, "team": "enemy", "type": drone_type,
            "position": {
                "x": random.uniform(SPAWN_PADDING, WORLD_WIDTH - SPAWN_PADDING),
                "y": random.uniform(SPAWN_PADDING, SPAWN_PADDING + 150)
            }
        })
    
    return {
        "name": blueprint["name"],
        "friendly_drones": friendly_drones,
        "enemy_drones": enemy_drones,
        "assets": assets
    }