# api/simulation_endpoints.py

import asyncio  # <-- This import is essential for the WebSocket logic
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from manager.simulation_manager import SimulationManager
from schemas.api_schemas import Command, ScenarioInfo
from services.scenario_service import get_scenario_list
from core import config

router = APIRouter()

@router.get("/api/scenarios", response_model=List[ScenarioInfo], tags=["Scenarios"])
def list_scenarios():
    """Provides the list of available scenarios to the GUI."""
    return get_scenario_list()

@router.websocket("/simulation")
async def simulation_websocket(websocket: WebSocket):
    """Handles simulation loop via WebSocket."""
    await websocket.accept()
    print("Client connected to simulation WebSocket.")
    manager = SimulationManager()

    try:
        while True:
            try:
                # Non-blocking wait for a command from the client
                command_json = await asyncio.wait_for(
                    websocket.receive_json(), 
                    timeout=config.DELTA_TIME
                )
                command = Command(**command_json)

                if command.command == "start":
                        # If custom counts are provided, use the new method
                        if command.num_friendly is not None and command.num_enemy is not None:
                            manager.start_custom(command.num_friendly, command.num_enemy)
                        # Otherwise, fall back to the old scenario ID logic
                        elif command.scenario_id:
                            manager.start(command.scenario_id)

                elif command.command == "pause":
                        manager.pause()
                    
                    # --- ADD THESE TWO BLOCKS ---
                elif command.command == "resume":
                        manager.resume()

                elif command.command == "reset":
                        manager.reset()
                    # -----------------------------

            except asyncio.TimeoutError:
                # This is normal - no command was received, so we just proceed
                pass
            except WebSocketDisconnect:
                # Handle client disconnecting gracefully
                break

            # Always update the simulation state
            state = manager.update()

            # Send the new state to the client
            await websocket.send_json(state.dict())

            # Wait for the next frame
            await asyncio.sleep(config.DELTA_TIME)

    except WebSocketDisconnect:
        print("Client disconnected from simulation WebSocket.")
    except Exception as e:
        print(f"An unexpected error occurred in the simulation loop: {e}")
    finally:
        manager.reset()
        print("Simulation session ended and manager has been reset.")
