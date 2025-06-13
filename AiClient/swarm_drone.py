import airsim
import time

print("Connecting to AirSim...")
# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()
print("Connected to AirSim!")

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

print("\nMoving drones up slightly...")
# Move drones upward a small amount
client.moveByVelocityAsync(0, 0, -2, 5, vehicle_name="Drone1").join()
client.moveByVelocityAsync(0, 0, -2, 5, vehicle_name="Drone2").join()
client.moveByVelocityAsync(0, 0, -2, 5, vehicle_name="Drone3").join()

# Check positions after upward movement
pos1 = client.getMultirotorState(vehicle_name="Drone1").kinematics_estimated.position
pos2 = client.getMultirotorState(vehicle_name="Drone2").kinematics_estimated.position
pos3 = client.getMultirotorState(vehicle_name="Drone3").kinematics_estimated.position
print(f"\nPositions after upward movement:")
print(f"Drone1: x={pos1.x_val:.2f}, y={pos1.y_val:.2f}, z={pos1.z_val:.2f}")
print(f"Drone2: x={pos2.x_val:.2f}, y={pos2.y_val:.2f}, z={pos2.z_val:.2f}")
print(f"Drone3: x={pos3.x_val:.2f}, y={pos3.y_val:.2f}, z={pos3.z_val:.2f}")

print("\nHovering for 3 seconds...")
time.sleep(3)

print("\nMoving drones down slightly...")
# Move drones downward a small amount
client.moveByVelocityAsync(0, 0, 2, 5, vehicle_name="Drone1").join()
client.moveByVelocityAsync(0, 0, 2, 5, vehicle_name="Drone2").join()
client.moveByVelocityAsync(0, 0, 2, 5, vehicle_name="Drone3").join()

# Check positions after downward movement
pos1 = client.getMultirotorState(vehicle_name="Drone1").kinematics_estimated.position
pos2 = client.getMultirotorState(vehicle_name="Drone2").kinematics_estimated.position
pos3 = client.getMultirotorState(vehicle_name="Drone3").kinematics_estimated.position
print(f"\nPositions after downward movement:")
print(f"Drone1: x={pos1.x_val:.2f}, y={pos1.y_val:.2f}, z={pos1.z_val:.2f}")
print(f"Drone2: x={pos2.x_val:.2f}, y={pos2.y_val:.2f}, z={pos2.z_val:.2f}")
print(f"Drone3: x={pos3.x_val:.2f}, y={pos3.y_val:.2f}, z={pos3.z_val:.2f}")

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