import airsim
import numpy as np
import time
import math

# Connect to AirSim
client = airsim.MultirotorClient(ip="127.0.0.1", port=41451)
client.confirmConnection()
print("Connected to AirSim!")

# Enable API control
client.enableApiControl(True, "Drone1")
client.armDisarm(True, "Drone1")

# Take off
print("Taking off...")
client.takeoffAsync(vehicle_name="Drone1").join()
client.moveToPositionAsync(0, 0, -3, 5, vehicle_name="Drone1").join()  # Adjusted takeoff height

# Wait for sensors
print("Waiting for sensors...")
time.sleep(2)

# Spiral flight parameters
radius = 5.0  # Initial radius of spiral
height = -3.0  # Starting height (reduced from -5.0)
angular_speed = 0.5  # Radians per second
height_increment = 0.03  # Reduced climb per step (was 0.05)
duration = 30  # Seconds

# Main loop: Spiral flight with obstacle check
print("Starting cinematic spiral flight...")
start_time = time.time()
while time.time() - start_time < duration:
    elapsed = time.time() - start_time
    angle = angular_speed * elapsed
    radius_current = radius * (1 - elapsed / duration)  # Shrink radius over time
    x = radius_current * math.cos(angle)
    y = radius_current * math.sin(angle)
    z = height + height_increment * elapsed

    # Get LIDAR data for safety
    lidar_data = client.getLidarData(lidar_name="Lidar1", vehicle_name="Drone1")
    if lidar_data.point_cloud:
        points = np.array(lidar_data.point_cloud).reshape(-1, 3)
        obstacles_ahead = [p for p in points if 0 < p[0] < 3 and abs(p[1]) < 1]
        if obstacles_ahead:
            print("Obstacle ahead! Adjusting height...")
            z += 0.5  # Reduced emergency climb (was 1)

    # Move to position
    client.moveToPositionAsync(x, y, z, 2, vehicle_name="Drone1").join()
    print(f"Moving to: ({x:.2f}, {y:.2f}, {z:.2f})")

    time.sleep(0.1)

# Land
print("Landing...")
client.landAsync(vehicle_name="Drone1").join()
client.armDisarm(False, "Drone1")
client.enableApiControl(False, "Drone1")
print("Done!")