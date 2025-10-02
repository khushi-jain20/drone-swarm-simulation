# backend/manager/simulation_manager.py
import time, uuid, csv, os
from datetime import datetime
from collections import Counter, defaultdict
from typing import List, Dict, Optional
import random

from schemas.common_schemas import Drone, Asset, Position, VisualEvent
from schemas.api_schemas import SimulationStreamData, AnalysisData, CoordinationTarget, SwarmStateSummary
from services import scenario_service, ai_service, physics_service
from core import config
from services.ai_service import SAFE_POINT

class SimulationManager:
    def __init__(self):
        self.reset()

    def reset(self):
        if hasattr(self, 'status') and self.status in ['running', 'paused', 'finished']: self._save_results_to_csv()
        self.status: str = "idle"; self.start_time: float = 0.0; self.scenario_id: Optional[str] = None
        self.friendly_drones: List[Drone] = []; self.enemy_drones: List[Drone] = []; self.assets: List[Asset] = []
        self.visual_events: List[VisualEvent] = []; self.event_log: List[Dict] = []; self.metrics: Dict = {}
        self.weapon_cooldowns: Dict[str, float] = {}; self.pending_damage: Dict[str, List[int]] = defaultdict(list)
        self.vengeance_buff_active: bool = False; self.vengeance_buff_timer: float = 0.0
        self.interception_times: List[float] = []
        self.percent_unattended_hostiles: float = 0.0
        self._reset_metrics()

    def _reset_metrics(self):
        self.metrics = {
            "assets_saved": 0, "neutralizations": 0, "friendly_losses": 0,
            "avg_interception_time": 0.0, "percent_unattended_hostiles": 0.0
        }

    def start_custom(self, num_friendly: int, num_enemy: int):
        scenario = scenario_service.generate_custom_scenario(num_friendly, num_enemy)
        self._load_and_run_scenario(scenario)

    def _load_and_run_scenario(self, scenario: Dict):
        self.reset()
        if not scenario: self.status = "idle"; return
        self.status = "running"; self.start_time = time.time()
        self.scenario_id = scenario.get("name", "Custom Battle")
        self.friendly_drones = [Drone(**d) for d in scenario["friendly_drones"]]
        self.enemy_drones = [Drone(**d) for d in scenario["enemy_drones"]]
        self.assets = [Asset(**a) for a in scenario["assets"]]
        self._reset_metrics(); self.metrics['assets_saved'] = len(self.assets)
        self.log_event(f"Simulation started: {self.scenario_id}")

    def pause(self):
        if self.status == 'running': self.status = 'paused'

    def resume(self):
        if self.status == 'paused': self.status = 'running'

    # Add this method inside the SimulationManager class

    def _handle_communication(self):
        """Simulates communication for Advanced AI, creating logs and visual events."""
        # Only run this logic for the advanced AI level
        if config.AI_INTELLIGENCE_LEVEL != 'advanced' or not self.friendly_drones:
            return

        # To avoid spamming, only a few drones communicate each tick
        if random.random() > 0.05: # 5% chance per tick to generate a comms event
            return

        source_drone = random.choice(self.friendly_drones)
        
        # Find nearby friendlies within communication range
        nearby_friendlies = [
            d for d in self.friendly_drones 
            if d.id != source_drone.id and 
            physics_service.calculate_distance(source_drone.position, d.position) <= config.COMMUNICATION_RANGE
        ]

        if not nearby_friendlies:
            return

        target_drone = random.choice(nearby_friendlies)

        # Log the event for the Communication Panel
        self.log_event(f"{source_drone.id} shared target data with {target_drone.id}")

        # Create a visual event to be rendered on the frontend
        self.visual_events.append(VisualEvent(
            id=str(uuid.uuid4()),
            type="comm_link",
            position=source_drone.position,
            target_position=target_drone.position,
            ttl=0.5, # Link will last for 0.5 seconds
            team='friendly'
        ))

    def update(self):
        effective_dt = float(config.DELTA_TIME * config.SPEED_MULTIPLIER)
        if self.status == "running":
            if self.vengeance_buff_active:
                self.vengeance_buff_timer -= effective_dt
                if self.vengeance_buff_timer <= 0:
                    self.vengeance_buff_active = False; self.log_event("Vengeance buff worn off.")
            self._handle_communication() 
            
            self._apply_pending_damage()
            all_drones = self.friendly_drones + self.enemy_drones
            self._apply_pending_damage()
            all_drones = self.friendly_drones + self.enemy_drones; drone_map = {d.id: d for d in all_drones}
            friendly_decisions = ai_service.get_swarm_decisions(self.friendly_drones, self.enemy_drones, self.assets)
            enemy_decisions = ai_service.get_enemy_decisions(self.enemy_drones, self.friendly_drones, self.assets)
            for drone_id, decision in {**friendly_decisions, **enemy_decisions}.items():
                drone = drone_map.get(drone_id)
                if drone: drone.status = decision.get("status", drone.status); drone.target_id = decision.get("target_id", drone.target_id)
            
            if self.enemy_drones:
                friendly_target_ids = {f.target_id for f in self.friendly_drones}
                unattended_count = sum(1 for e in self.enemy_drones if e.id not in friendly_target_ids)
                self.percent_unattended_hostiles = (unattended_count / len(self.enemy_drones)) * 100
            else:
                self.percent_unattended_hostiles = 0.0
            
            for drone in all_drones:
                drone_speed = config.FRIENDLY_DRONE_SPEED if drone.team == 'friendly' else config.ENEMY_DRONE_SPEED
                if drone.status == "retreating": drone.position, drone.velocity = physics_service.move_towards(drone.position, SAFE_POINT, drone_speed, effective_dt); continue
                target = drone_map.get(drone.target_id)
                if drone.status in ["engaging", "intercepting"] and target:
                    intercept_point = physics_service.calculate_intercept_point(drone.position, target.position, getattr(target, 'velocity', None), drone_speed)
                    drone.position, drone.velocity = physics_service.move_towards(drone.position, intercept_point, drone_speed, effective_dt)
                else: drone.velocity = Position(x=0.0, y=0.0)
            self._handle_combat()
            if not self.enemy_drones or not self.friendly_drones or all(asset.health <= 0 for asset in self.assets):
                self.status = "finished"; self.log_event("Simulation finished.")
        return self.get_current_state()

   # backend/manager/simulation_manager.py
# (Only showing the changed method, the rest of the file is correct from the last version)

# ... (all other methods remain the same) ...

    def _handle_combat(self):
        all_drones = self.friendly_drones + self.enemy_drones
        drone_map = {d.id: d for d in all_drones}
        now = time.time()
        
        for drone in all_drones:
            # --- NO MORE BUFFS ---
            # All units now use the base weapon stats from the config file.
            # Victory is determined by AI logic alone.
            current_cooldown = config.WEAPON_COOLDOWN
            current_damage = config.WEAPON_DAMAGE
            # --------------------
            
            if drone.status in ["engaging", "intercepting"] and drone.target_id and (now - self.weapon_cooldowns.get(drone.id, 0) > current_cooldown):
                target = drone_map.get(drone.target_id)
                if target and physics_service.calculate_distance(drone.position, target.position) <= config.FIRING_RANGE:
                    self.visual_events.append(VisualEvent(id=str(uuid.uuid4()), type="weapon_fire", position=drone.position, target_position=target.position, ttl=0.25, team=drone.team))
                    self.pending_damage[target.id].append(current_damage)
                    self.weapon_cooldowns[drone.id] = now

    def _apply_pending_damage(self):
        if not self.pending_damage: return
        all_drones = self.friendly_drones + self.enemy_drones; drone_map = {d.id: d for d in all_drones}
        drones_to_remove = set()
        for target_id, damage_list in self.pending_damage.items():
            target = drone_map.get(target_id)
            if target and target.health > 0:
                target.health -= sum(damage_list)
                if target.health <= 0:
                    self.log_event(f"{target.id} neutralized!"); drones_to_remove.add(target.id)
                    self.visual_events.append(VisualEvent(id=str(uuid.uuid4()), type="neutralization", position=target.position, ttl=1.5, team=getattr(target, 'team', 'asset')))
        if drones_to_remove:
            sim_time = (time.time() - self.start_time) if self.start_time > 0 else 0
            for removed_id in drones_to_remove:
                removed_drone = drone_map.get(removed_id)
                if removed_drone:
                    if removed_drone.team == "friendly":
                        self.metrics["friendly_losses"] += 1
                        if not self.vengeance_buff_active and config.AI_INTELLIGENCE_LEVEL != 'advanced':
                           self.log_event("Vengeance protocol activated!"); self.vengeance_buff_active = True; self.vengeance_buff_timer = 10.0
                    else:
                        self.metrics["neutralizations"] += 1
                        self.interception_times.append(sim_time)
            self.friendly_drones = [d for d in self.friendly_drones if d.id not in drones_to_remove]
            self.enemy_drones = [d for d in self.enemy_drones if d.id not in drones_to_remove]
        self.pending_damage.clear()

    def get_current_state(self) -> SimulationStreamData:
        sim_time = (time.time() - self.start_time) if self.start_time > 0 else 0
        self.visual_events = [e for e in self.visual_events if e.ttl > 0]
        for e in self.visual_events: e.ttl -= float(config.DELTA_TIME * config.SPEED_MULTIPLIER)
        avg_intercept_time = sum(self.interception_times) / len(self.interception_times) if self.interception_times else 0
        self.metrics["avg_interception_time"] = avg_intercept_time
        self.metrics["percent_unattended_hostiles"] = self.percent_unattended_hostiles
        return SimulationStreamData(simulation_state={"status": self.status, "time": sim_time}, drones=[d.dict() for d in self.friendly_drones + self.enemy_drones], assets=[a.dict() for a in self.assets], visual_events=[e.dict() for e in self.visual_events], metrics=self.metrics, event_log=self.event_log[-20:], analysis=self._get_analysis_data())

    def _get_analysis_data(self) -> AnalysisData:
        drone_map = {d.id: d for d in self.friendly_drones + self.enemy_drones}
        targets = [CoordinationTarget(source_id=d.id, target_id=d.target_id, distance=int(physics_service.calculate_distance(d.position, drone_map[d.target_id].position))) for d in self.friendly_drones if getattr(d, 'target_id', None) and d.target_id in drone_map]
        return AnalysisData(coordination_targets=targets, swarm_state=[])

    def log_event(self, message: str):
        sim_time = (time.time() - self.start_time) if self.start_time > 0 else 0
        self.event_log.append({"time": round(sim_time, 1), "message": message})

    def _save_results_to_csv(self):
        if not self.scenario_id: return
        sim_time = (time.time() - self.start_time) if self.start_time > 0 else 0
        header = ["timestamp", "scenario_id", "sim_time_sec", "neutralizations", "friendly_losses", "assets_saved", "avg_intercept_time"]
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "scenario_id": self.scenario_id, 
            "sim_time_sec": round(sim_time, 2), "neutralizations": self.metrics["neutralizations"], 
            "friendly_losses": self.metrics["friendly_losses"], "assets_saved": self.metrics["assets_saved"],
            "avg_intercept_time": round(self.metrics["avg_interception_time"], 2)
        }
        try:
            file_exists = os.path.isfile(config.RESULTS_CSV_PATH)
            with open(config.RESULTS_CSV_PATH, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=header)
                if not file_exists: writer.writeheader()
                writer.writerow(data)
        except IOError as e: print(f"[CSV Logger] Error: {e}")