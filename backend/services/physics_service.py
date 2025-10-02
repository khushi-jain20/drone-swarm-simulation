# services/physics_service.py
from typing import Tuple
import numpy as np
from schemas.common_schemas import Position
from core import config

def calculate_distance(pos1: Position, pos2: Position) -> float:
    """Calculates the Euclidean distance between two positions."""
    # Ensure positions are numpy arrays for vector operations
    pos1_np = np.array([pos1.x, pos1.y])
    pos2_np = np.array([pos2.x, pos2.y])
    return np.linalg.norm(pos1_np - pos2_np)

def move_towards(current_pos: Position, target_pos: Position, max_speed: float, dt: float) -> Tuple[Position, Position]:
    """
    Calculates the new position and velocity for the next tick, correctly using the provided delta-time (dt).
    Returns: (new_position, new_velocity)
    """
    if not target_pos:
        return current_pos, Position(x=0.0, y=0.0)

    current_np = np.array([current_pos.x, current_pos.y])
    target_np = np.array([target_pos.x, target_pos.y])
    
    direction = target_np - current_np
    distance = np.linalg.norm(direction)

    # If already at or very close to the target, don't move
    if distance < 1.0:
        return current_pos, Position(x=0.0, y=0.0)

    # Normalize the direction vector to get a unit vector
    unit_direction = direction / distance
    
    # Calculate the velocity vector
    velocity_np = unit_direction * max_speed
    
    # Calculate the new position based on velocity and the provided delta-time
    new_pos_np = current_np + velocity_np * dt

    # Check if we have overshot the target in this frame
    if np.linalg.norm(new_pos_np - current_np) > distance:
        new_pos_np = target_np  # If so, clamp position to the target

    # Return the new position and the calculated velocity as Pydantic models
    new_position = Position(x=float(new_pos_np[0]), y=float(new_pos_np[1]))
    velocity = Position(x=float(velocity_np[0]), y=float(velocity_np[1]))
    
    return new_position, velocity

def calculate_intercept_point(interceptor_pos: Position, target_pos: Position, target_vel: Position, interceptor_speed: float) -> Position:
    """
    Calculates the future position to intercept a moving target.
    (This function is mathematically sound and remains unchanged).
    """
    target_pos_np = np.array([target_pos.x, target_pos.y])
    target_vel_np = np.array([target_vel.x, target_vel.y]) if target_vel else np.array([0.0, 0.0])
    interceptor_pos_np = np.array([interceptor_pos.x, interceptor_pos.y])

    relative_pos = target_pos_np - interceptor_pos_np
    relative_vel = target_vel_np
    
    a = np.dot(relative_vel, relative_vel) - interceptor_speed ** 2
    b = 2 * np.dot(relative_vel, relative_pos)
    c = np.dot(relative_pos, relative_pos)
    
    discriminant = b**2 - 4 * a * c
    if discriminant < 0: return target_pos
    if abs(a) < 1e-6: return target_pos
    
    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
    
    positive_ts = [t for t in (t1, t2) if t > 0.01]
    if not positive_ts: return target_pos
    
    time_to_intercept = min(positive_ts)
    intercept_point = target_pos_np + target_vel_np * time_to_intercept
    
    return Position(x=float(intercept_point[0]), y=float(intercept_point[1]))


# Add this function to your existing physics_service.py file

def calculate_time_to_intercept(interceptor_pos: Position, target_pos: Position, target_vel: Position, interceptor_speed: float) -> float:
    """Calculates the time it will take for an interceptor to reach a target."""
    target_pos_np = np.array([target_pos.x, target_pos.y])
    target_vel_np = np.array([target_vel.x, target_vel.y]) if target_vel else np.array([0.0, 0.0])
    interceptor_pos_np = np.array([interceptor_pos.x, interceptor_pos.y])

    relative_pos = target_pos_np - interceptor_pos_np
    
    a = np.dot(target_vel_np, target_vel_np) - interceptor_speed ** 2
    b = 2 * np.dot(target_vel_np, relative_pos)
    c = np.dot(relative_pos, relative_pos)
    
    discriminant = b**2 - 4 * a * c
    if discriminant < 0: return float('inf')
    if abs(a) < 1e-6: return float('inf')
    
    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
    
    positive_times = [t for t in (t1, t2) if t > 0.01]
    return min(positive_times) if positive_times else float('inf')

