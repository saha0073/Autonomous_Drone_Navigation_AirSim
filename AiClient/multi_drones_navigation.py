import airsim
import time
import math
import numpy as np
import sys

def connect_with_retry(max_retries=30, retry_delay=2):
    """Attempt to connect to AirSim with retries"""
    print("Attempting to connect to AirSim...")
    for attempt in range(max_retries):
        try:
            client = airsim.MultirotorClient()
            client.confirmConnection()
            print("Successfully connected to AirSim!")
            return client
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1}/{max_retries} failed. Retrying in {retry_delay} seconds...")
                print(f"Error: {str(e)}")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect after {max_retries} attempts.")
                print("Please make sure AirSim is running and try again.")
                sys.exit(1)

# Connect to AirSim with retry logic
client = connect_with_retry(max_retries=30, retry_delay=2)

# Verify available vehicles
print("\nChecking available vehicles...")
vehicles = client.listVehicles()
print(f"Available vehicles: {vehicles}")

if len(vehicles) < 3:
    print("Error: Not enough vehicles found! Please check your settings.json")
    exit()

print("\nEnabling API control for drones...")
# Enable API control for all drones
client.enableApiControl(True, "Drone1")
client.enableApiControl(True, "Drone2")
client.enableApiControl(True, "Drone3")
print("API control enabled!")

print("\nArming drones...")
# Arm the drones
client.armDisarm(True, "Drone1")
client.armDisarm(True, "Drone2")
client.armDisarm(True, "Drone3")
print("Drones armed!")

print("\nTaking off...")
# Take off
client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()
client.takeoffAsync(vehicle_name="Drone3").join()
print("Takeoff complete!")

# Get initial positions
pos1 = client.getMultirotorState(vehicle_name="Drone1").kinematics_estimated.position
pos2 = client.getMultirotorState(vehicle_name="Drone2").kinematics_estimated.position
pos3 = client.getMultirotorState(vehicle_name="Drone3").kinematics_estimated.position
print(f"\nInitial positions:")
print(f"Drone1: x={pos1.x_val:.2f}, y={pos1.y_val:.2f}, z={pos1.z_val:.2f}")
print(f"Drone2: x={pos2.x_val:.2f}, y={pos2.y_val:.2f}, z={pos2.z_val:.2f}")
print(f"Drone3: x={pos3.x_val:.2f}, y={pos3.y_val:.2f}, z={pos3.z_val:.2f}")

# Complex swarm parameters
base_radius = 5.0  # Base radius of the spiral
height_range = (-4.0, -2.0)  # Height range for vertical movement
angular_speed = 0.8  # Increased from 0.3 to 0.8 radians per second
spiral_speed = 0.3  # Increased from 0.1 to 0.3 for faster spiral changes
duration = 20  # Reduced from 30 to 20 seconds for faster overall pattern
swap_interval = 10  # Time between position swaps

print("\nStarting complex swarm formation...")
start_time = time.time()

def calculate_position(elapsed, drone_index):
    # Calculate base angle with offset for each drone
    angle = angular_speed * elapsed + (2 * math.pi / 3 * drone_index)
    
    # Calculate spiral radius that changes over time
    radius = base_radius * (1 + math.sin(spiral_speed * elapsed))
    
    # Calculate vertical position with smooth oscillation
    height = (height_range[0] + height_range[1]) / 2 + \
             (height_range[1] - height_range[0]) / 2 * math.sin(angular_speed * elapsed)
    
    # Calculate x, y positions with spiral
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    
    return x, y, height

try:
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        
        # Calculate positions for each drone
        positions = []
        for i in range(3):
            x, y, z = calculate_position(elapsed, i)
            positions.append((x, y, z))
        
        # Move drones to their positions
        for i, (x, y, z) in enumerate(positions):
            drone_name = f"Drone{i+1}"
            client.moveToPositionAsync(x, y, z, 1.5, vehicle_name=drone_name).join()  # Reduced from 2 to 1.5 for faster movement
        
        # Print current positions
        pos1 = client.getMultirotorState(vehicle_name="Drone1").kinematics_estimated.position
        pos2 = client.getMultirotorState(vehicle_name="Drone2").kinematics_estimated.position
        pos3 = client.getMultirotorState(vehicle_name="Drone3").kinematics_estimated.position
        print(f"\nCurrent positions at {elapsed:.1f}s:")
        print(f"Drone1: x={pos1.x_val:.2f}, y={pos1.y_val:.2f}, z={pos1.z_val:.2f}")
        print(f"Drone2: x={pos2.x_val:.2f}, y={pos2.y_val:.2f}, z={pos2.z_val:.2f}")
        print(f"Drone3: x={pos3.x_val:.2f}, y={pos3.y_val:.2f}, z={pos3.z_val:.2f}")
        
        time.sleep(0.05)  # Reduced from 0.1 to 0.05 for more frequent updates

except Exception as e:
    print(f"\nAn error occurred during flight: {str(e)}")
    print("Attempting to land drones safely...")
    try:
        client.landAsync(vehicle_name="Drone1").join()
        client.landAsync(vehicle_name="Drone2").join()
        client.landAsync(vehicle_name="Drone3").join()
    except:
        print("Emergency landing failed. Please check drone status manually.")
    sys.exit(1)

print("\nHovering for 3 seconds...")
time.sleep(3)

print("\nLanding drones...")
# Land
client.landAsync(vehicle_name="Drone1").join()
client.landAsync(vehicle_name="Drone2").join()
client.landAsync(vehicle_name="Drone3").join()
print("Landing complete!")

# Check final positions
pos1 = client.getMultirotorState(vehicle_name="Drone1").kinematics_estimated.position
pos2 = client.getMultirotorState(vehicle_name="Drone2").kinematics_estimated.position
pos3 = client.getMultirotorState(vehicle_name="Drone3").kinematics_estimated.position
print(f"\nFinal positions:")
print(f"Drone1: x={pos1.x_val:.2f}, y={pos1.y_val:.2f}, z={pos1.z_val:.2f}")
print(f"Drone2: x={pos2.x_val:.2f}, y={pos2.y_val:.2f}, z={pos2.z_val:.2f}")
print(f"Drone3: x={pos3.x_val:.2f}, y={pos3.y_val:.2f}, z={pos3.z_val:.2f}")

print("\nDisarming drones...")
# Disarm
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")
client.armDisarm(False, "Drone3")
print("Drones disarmed!")

print("\nDisabling API control...")
# Disable API control
client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
client.enableApiControl(False, "Drone3")
print("API control disabled!")

print("\nMission complete!")