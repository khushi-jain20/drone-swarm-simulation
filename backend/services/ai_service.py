# backend/services/ai_service.py
from typing import List, Dict, Set, Optional
from schemas.common_schemas import Drone, Asset, Position
from services.physics_service import calculate_distance, calculate_time_to_intercept
from core import config
import random

# --- MAIN AI ROUTER ---
def get_swarm_decisions(friendly_drones: List[Drone], enemy_drones: List[Drone], assets: List[Asset]) -> Dict[str, Dict]:
    level = config.AI_INTELLIGENCE_LEVEL
    if level == 'basic': return _get_basic_decisions(friendly_drones, enemy_drones)
    elif level in ('advanced', 'adaptive'): return _get_ultimate_strategy_decisions(friendly_drones, enemy_drones, assets)
    else: return _get_normal_decisions(friendly_drones, enemy_drones, assets)

# --- ENEMY AI LOGIC (Remains coordinated) ---
def get_enemy_decisions(enemy_drones: List[Drone], friendly_drones: List[Drone], assets: List[Asset]) -> Dict[str, Dict]:
    # ... (this logic is unchanged from the last version)
    decisions = {}
    if not friendly_drones and not assets: return {e.id: {"status": "patrolling"} for e in enemy_drones}
    primary_target: Optional[Drone] = None
    if assets and friendly_drones: primary_target = min(friendly_drones, key=lambda f: min(calculate_distance(f.position, a.position) for a in assets))
    assigned_drones = set(); num_focus_fire = len(enemy_drones) // 2
    if primary_target:
        enemies_by_distance = sorted(enemy_drones, key=lambda e: calculate_distance(e.position, primary_target.position))
        for i in range(min(num_focus_fire, len(enemies_by_distance))):
            drone = enemies_by_distance[i]; decisions[drone.id] = {"status": "engaging", "target_id": primary_target.id}; assigned_drones.add(drone.id)
    for enemy in enemy_drones:
        if enemy.id in assigned_drones: continue
        if enemy.type == 'ground_attack' and assets: decisions[enemy.id] = {"status": "engaging", "target_id": min(assets, key=lambda a: calculate_distance(enemy.position, a.position)).id}
        elif friendly_drones: decisions[enemy.id] = {"status": "engaging", "target_id": min(friendly_drones, key=lambda f: calculate_distance(enemy.position, f.position)).id}
        else: decisions[enemy.id] = {"status": "patrolling"}
    return decisions

# ---  LEVEL 1: BASIC (Simple and greedy) ---
def _get_basic_decisions(friendly_drones: List[Drone], enemy_drones: List[Drone]) -> Dict[str, Dict]:
    decisions = {}
    if not enemy_drones: return {f.id: {"status": "patrolling"} for f in friendly_drones}
    for f_drone in friendly_drones:
        closest_enemy = min(enemy_drones, key=lambda e: calculate_distance(f_drone.position, e.position))
        decisions[f_drone.id] = {"status": "engaging", "target_id": closest_enemy.id}
    return decisions

# --- LEVEL 2: NORMAL (Threat-based but uncoordinated) ---
def _get_normal_decisions(friendly_drones: List[Drone], enemy_drones: List[Drone], assets: List[Asset]) -> Dict[str, Dict]:
    decisions = {}
    if not enemy_drones: return {f.id: {"status": "patrolling"} for f in friendly_drones}
    for f_drone in friendly_drones:
        threats = sorted(enemy_drones, key=lambda e: calculate_distance(f_drone.position, e.position))
        if assets:
            threats = sorted(threats, key=lambda e: min(calculate_distance(e.position, a.position) for a in assets) if e.type == 'ground_attack' else float('inf'))
        decisions[f_drone.id] = {"status": "engaging", "target_id": threats[0].id}
    return decisions

# ---  LEVEL 3: ADVANCED (The Unbeatable Tactician) ---
SAFE_POINT = Position(x=config.WORLD_WIDTH / 2, y=config.WORLD_HEIGHT - 50)
CRITICAL_HEALTH_THRESHOLD = 25; NUM_GUARDIANS = 3; GUARDIAN_ZONE_RADIUS = config.THREATENING_RANGE * 1.5

def _get_advanced_threat_score(enemy: Drone, assets: List[Asset]) -> float:
    score = 1000.0 / (calculate_distance(enemy.position, assets[0].position) + 1) if assets and enemy.type == 'ground_attack' else 1.0
    if enemy.health < 100: score *= 2.0
    return score

def _get_ultimate_strategy_decisions(friendly_drones: List[Drone], enemy_drones: List[Drone], assets: List[Asset]) -> Dict[str, Dict]:
    decisions, assigned_drones = {}, set()
    if not enemy_drones: return {f.id: {"status": "patrolling"} for f in friendly_drones}

    drones_by_asset_proximity = sorted(friendly_drones, key=lambda f: min((calculate_distance(f.position, a.position) for a in assets), default=float('inf')))
    guardians = drones_by_asset_proximity[:NUM_GUARDIANS]; hunters = drones_by_asset_proximity[NUM_GUARDIANS:]
    
    # Guardian Logic
    enemies_in_zone = [e for e in enemy_drones if any(calculate_distance(e.position, a.position) < GUARDIAN_ZONE_RADIUS for a in assets)]
    for g in guardians:
        if enemies_in_zone:
            threat = min(enemies_in_zone, key=lambda e: calculate_distance(g.position, e.position))
            decisions[g.id] = {"status": "intercepting", "target_id": threat.id}; assigned_drones.add(g.id)
        else: decisions[g.id] = {"status": "patrolling"}

    # Hunter Logic: Optimal Target Allocation
    available_hunters = [h for h in hunters if h.id not in assigned_drones]
    enemy_threats = sorted(enemy_drones, key=lambda e: _get_advanced_threat_score(e, assets), reverse=True)
    
    for threat in enemy_threats:
        if not available_hunters: break
        # Find the single best hunter for this specific threat
        best_hunter = min(available_hunters, key=lambda h: calculate_time_to_intercept(h.position, threat.position, threat.velocity, config.FRIENDLY_DRONE_SPEED))
        decisions[best_hunter.id] = {"status": "engaging", "target_id": threat.id}
        assigned_drones.add(best_hunter.id)
        available_hunters.remove(best_hunter)

    # Assign any remaining drones
    for drone in friendly_drones:
        if drone.id not in decisions: decisions[drone.id] = {"status": "patrolling"}
        
    return decisions
