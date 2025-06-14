import airsim
import time
import math
import numpy as np
import sys
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class DroneState:
    position: Tuple[float, float, float]
    velocity: Tuple[float, float, float]
    battery: float
    obstacles: List[Tuple[float, float, float]]

class SwarmController:
    def __init__(self, client: airsim.MultirotorClient, drone_names: List[str]):
        self.client = client
        self.drone_names = drone_names
        self.drone_states: Dict[str, DroneState] = {}
        self.safety_distance = 2.0  # Minimum distance between drones
        self.formation_radius = 5.0
        self.swarm_center = (0, 0, -3)
        self.formation_type = "circle"  # Can be "circle", "spiral", "wave", "diamond"
        self.formation_phase = 0
        print(f"\nInitializing Swarm Controller with drones: {drone_names}")
        
    def update_drone_states(self):
        """Update state information for all drones"""
        print("\nUpdating drone states...")
        for drone_name in self.drone_names:
            try:
                state = self.client.getMultirotorState(vehicle_name=drone_name)
                pos = state.kinematics_estimated.position
                vel = state.kinematics_estimated.linear_velocity
                
                # Get LIDAR data for obstacle detection
                lidar_data = self.client.getLidarData(lidar_name="Lidar1", vehicle_name=drone_name)
                obstacles = []
                if lidar_data.point_cloud:
                    points = np.array(lidar_data.point_cloud).reshape(-1, 3)
                    obstacles = [tuple(p) for p in points if np.linalg.norm(p) < 3.0]
                
                self.drone_states[drone_name] = DroneState(
                    position=(pos.x_val, pos.y_val, pos.z_val),
                    velocity=(vel.x_val, vel.y_val, vel.z_val),
                    battery=100.0,  # Placeholder for battery level
                    obstacles=obstacles
                )
                
                print(f"\n{drone_name} State:")
                print(f"  Position: x={pos.x_val:.2f}, y={pos.y_val:.2f}, z={pos.z_val:.2f}")
                print(f"  Velocity: x={vel.x_val:.2f}, y={vel.y_val:.2f}, z={vel.z_val:.2f}")
                print(f"  Obstacles detected: {len(obstacles)}")
                
            except Exception as e:
                print(f"Error updating state for {drone_name}: {str(e)}")
    
    def check_collision_risk(self, drone_name: str, target_pos: Tuple[float, float, float]) -> bool:
        """Check if moving to target position would cause collision with other drones"""
        current_pos = self.drone_states[drone_name].position
        for other_drone, other_state in self.drone_states.items():
            if other_drone != drone_name:
                dist = np.linalg.norm(np.array(target_pos) - np.array(other_state.position))
                if dist < self.safety_distance:
                    print(f"\nCollision risk detected:")
                    print(f"  {drone_name} -> {other_drone}")
                    print(f"  Distance: {dist:.2f}m (minimum: {self.safety_distance}m)")
                    return True
        return False
    
    def calculate_swarm_center(self) -> Tuple[float, float, float]:
        """Calculate the center point of the swarm"""
        positions = [state.position for state in self.drone_states.values()]
        center = tuple(np.mean(positions, axis=0))
        print(f"\nSwarm Center: x={center[0]:.2f}, y={center[1]:.2f}, z={center[2]:.2f}")
        return center
    
    def calculate_formation_positions(self, center: Tuple[float, float, float], 
                                   angle: float) -> Dict[str, Tuple[float, float, float]]:
        """Calculate positions for each drone in the formation"""
        positions = {}
        print(f"\nCalculating formation positions (angle: {angle:.2f}):")
        
        # Change formation type periodically
        if int(angle / (2 * math.pi)) > self.formation_phase:
            self.formation_phase = int(angle / (2 * math.pi))
            formations = ["circle", "spiral", "wave", "diamond"]
            self.formation_type = formations[self.formation_phase % len(formations)]
            print(f"\nSwitching to {self.formation_type} formation!")
        
        for i, drone_name in enumerate(self.drone_names):
            if self.formation_type == "circle":
                # Circular formation
                offset_angle = angle + (2 * math.pi * i / len(self.drone_names))
                x = center[0] + self.formation_radius * math.cos(offset_angle)
                y = center[1] + self.formation_radius * math.sin(offset_angle)
                z = center[2] + 0.5 * math.sin(angle)
                
            elif self.formation_type == "spiral":
                # Spiral formation
                spiral_angle = angle + (2 * math.pi * i / len(self.drone_names))
                radius = self.formation_radius * (1 + 0.2 * math.sin(angle))
                x = center[0] + radius * math.cos(spiral_angle)
                y = center[1] + radius * math.sin(spiral_angle)
                z = center[2] + 1.0 * math.sin(spiral_angle)
                
            elif self.formation_type == "wave":
                # Wave formation
                wave_angle = angle + (2 * math.pi * i / len(self.drone_names))
                x = center[0] + self.formation_radius * math.cos(wave_angle)
                y = center[1] + self.formation_radius * math.sin(wave_angle)
                z = center[2] + 2.0 * math.sin(wave_angle + i)
                
            else:  # diamond formation
                # Diamond formation
                diamond_angle = angle + (2 * math.pi * i / len(self.drone_names))
                radius = self.formation_radius * (1 + 0.5 * math.sin(diamond_angle))
                x = center[0] + radius * math.cos(diamond_angle)
                y = center[1] + radius * math.sin(diamond_angle)
                z = center[2] + 1.0 * math.cos(diamond_angle)
            
            # Check for obstacles and adjust if necessary
            if self.drone_states[drone_name].obstacles:
                print(f"  {drone_name}: Obstacles detected, adjusting height")
                z += 0.5  # Rise above obstacles
            
            positions[drone_name] = (x, y, z)
            print(f"  {drone_name} target: x={x:.2f}, y={y:.2f}, z={z:.2f}")
        return positions
    
    def execute_swarm_movement(self, duration: float = 30.0):
        """Execute coordinated swarm movement"""
        print(f"\nStarting swarm movement for {duration} seconds")
        start_time = time.time()
        angular_speed = 0.5
        
        while time.time() - start_time < duration:
            try:
                # Update all drone states
                self.update_drone_states()
                
                # Calculate new swarm center
                self.swarm_center = self.calculate_swarm_center()
                
                # Calculate formation positions
                elapsed = time.time() - start_time
                angle = angular_speed * elapsed
                target_positions = self.calculate_formation_positions(self.swarm_center, angle)
                
                # Move each drone to its target position
                print("\nExecuting movement commands:")
                for drone_name, target_pos in target_positions.items():
                    if not self.check_collision_risk(drone_name, target_pos):
                        print(f"  Moving {drone_name} to: x={target_pos[0]:.2f}, y={target_pos[1]:.2f}, z={target_pos[2]:.2f}")
                        self.client.moveToPositionAsync(
                            target_pos[0], target_pos[1], target_pos[2],
                            2.0, vehicle_name=drone_name
                        ).join()
                    else:
                        print(f"  {drone_name}: Movement skipped due to collision risk")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"\nError during swarm movement: {str(e)}")
                print("Attempting to continue...")
                time.sleep(1)  # Wait a bit before retrying

def main():
    print("\nInitializing AirSim connection...")
    # Connect to AirSim
    client = airsim.MultirotorClient()
    client.confirmConnection()
    print("Connected to AirSim!")
    
    # Initialize drones
    drone_names = ["Drone1", "Drone2", "Drone3", "Drone4", "Drone5"]
    
    print("\nEnabling API control and arming drones...")
    # Enable API control and arm drones
    for drone_name in drone_names:
        try:
            print(f"\nSetting up {drone_name}:")
            print("  Enabling API control...")
            client.enableApiControl(True, drone_name)
            print("  Arming...")
            client.armDisarm(True, drone_name)
            print("  Taking off...")
            client.takeoffAsync(vehicle_name=drone_name).join()
            print(f"  {drone_name} is ready!")
        except Exception as e:
            print(f"Error during {drone_name} setup: {str(e)}")
            raise
    
    # Create swarm controller
    swarm = SwarmController(client, drone_names)
    
    try:
        # Execute swarm movement
        swarm.execute_swarm_movement(duration=30)
        
    except Exception as e:
        print(f"\nError during swarm operation: {str(e)}")
    finally:
        print("\nLanding drones...")
        # Land all drones
        for drone_name in drone_names:
            try:
                print(f"  Landing {drone_name}...")
                client.landAsync(vehicle_name=drone_name).join()
                print(f"  Disarming {drone_name}...")
                client.armDisarm(False, drone_name)
                print(f"  Disabling API control for {drone_name}...")
                client.enableApiControl(False, drone_name)
                print(f"  {drone_name} landed safely!")
            except Exception as e:
                print(f"Error during {drone_name} landing: {str(e)}")

if __name__ == "__main__":
    main()