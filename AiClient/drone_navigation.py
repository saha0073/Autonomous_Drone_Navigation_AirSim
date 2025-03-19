import airsim
import time
import numpy as np

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
client.moveToPositionAsync(0, 0, -5, 5, vehicle_name="Drone1").join()

# Wait briefly for sensors to initialize
print("Waiting for sensors to initialize...")
time.sleep(2)

# Main loop with obstacle avoidance
print("Starting obstacle avoidance flight...")
for _ in range(300):  # Run for ~30 seconds (0.1s per iteration)
    # Get LIDAR data
    lidar_data = client.getLidarData(lidar_name="Lidar1", vehicle_name="Drone1")
    print(f"LIDAR timestamp: {lidar_data.time_stamp}, Pose: {lidar_data.pose}")
    
    if lidar_data.point_cloud:
        points = np.array(lidar_data.point_cloud).reshape(-1, 3)
        print(f"Number of LIDAR points: {len(points)}")
        obstacles_ahead = [p for p in points if 0 < p[0] < 3 and abs(p[1]) < 1]
        
        if obstacles_ahead:
            min_distance = min(p[0] for p in obstacles_ahead)
            print(f"Obstacle detected {min_distance:.2f}m ahead! Ascending...")
            client.moveByVelocityAsync(0, 0, -1, 1, vehicle_name="Drone1").join()
        else:
            print("Path clear, moving forward...")
            client.moveByVelocityAsync(1, 0, 0, 1, vehicle_name="Drone1").join()
    else:
        print("No LIDAR data received!")

    time.sleep(0.1)

# Land
print("Landing...")
client.landAsync(vehicle_name="Drone1").join()
client.armDisarm(False, "Drone1")
client.enableApiControl(False, "Drone1")
print("Done!")