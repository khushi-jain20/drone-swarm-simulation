# backend/core/config.py

# --- Simulation Timing ---
# Rate at which the simulation updates (in seconds). 60Hz is a good target.
DELTA_TIME: float = 1 / 60.0
# Initial speed multiplier for the simulation (can be changed via API)
SPEED_MULTIPLIER: float = 1.0

# --- World & Scenario ---
# These MUST match the frontend canvas dimensions for correct positioning
WORLD_WIDTH: int = 1200
WORLD_HEIGHT: int = 800
# Path for saving simulation results
RESULTS_CSV_PATH: str = "simulation_results.csv"

# --- Drone Technical Specifications ---
# Speeds are in meters per second (or units per second)
FRIENDLY_DRONE_SPEED: float = 50.0
ENEMY_DRONE_SPEED: float = 50.0
# General max speed used for physics calculations
DRONE_MAX_SPEED: float = 50.0

# --- Combat Parameters ---
# --- FIX: Reduced firing range for closer combat ---
FIRING_RANGE: float = 250.0 # Old value was 500.0
# ---------------------------------------------------
WEAPON_COOLDOWN: float = 1.0  # seconds between shots
WEAPON_DAMAGE: int = 34 # 3-4 shots to neutralize a drone

# --- AI & Threat Logic ---
COMMUNICATION_RANGE: float = 400.0
# Threatening range definition: 10 times the speed of the enemy drone.
# This is the "red alert" zone around a ground asset.
THREATENING_RANGE: float = ENEMY_DRONE_SPEED * 10.0
# General sensor range for AI decisions (e.g., detecting nearby friendlies)
SENSOR_RANGE: float = 800.0
# Initial AI intelligence level (can be changed via API)
AI_INTELLIGENCE_LEVEL: str = "basic" # Options: basic, normal, advanced, adaptive