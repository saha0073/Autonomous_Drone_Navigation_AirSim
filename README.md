# Autonommous Drone Navigation with AirSim inside Unreal Engine

A dynamic drone navigation system that creates cinematic spiral flight patterns while incorporating real-time obstacle avoidance using LIDAR data using AirSim simulation inside Unreal Engine environment.

## Demo
[![Watch the Spiral Pattern Demo](https://img.youtube.com/vi/Szfl03-d1VI/0.jpg)](https://youtu.be/Szfl03-d1VI) 
[![Watch the Swarm Demo](https://img.youtube.com/vi/z0FzZgCPRPk/0.jpg)](https://youtu.be/z0FzZgCPRPk)

▶️ *Click to watch the demo videos on YouTube*

This project implements an autonomous drone control system that generates smooth, cinematic flight paths while maintaining safety through obstacle detection. The system supports both individual drone navigation with spiral patterns and coordinated swarm movements with multiple drones.

## Features
* Autonomous spiral flight pattern generation
* Real-time LIDAR-based obstacle detection and avoidance
* Smooth trajectory adjustments
* Configurable flight parameters
* Coordinated swarm movement with multiple drones
* Synchronized circular formation patterns

## Technical Stack
* Simulation Environment: Unreal Engine 5 with Colosseum AirSim plugin
* Programming Language: Python
* Libraries: AirSim Python API
* Sensors: LIDAR (16-channel)

## System Architecture

### Single Drone Navigation
The single drone system (`single_drone_navigation.py`) implements a cinematic spiral flight pattern with obstacle avoidance:

1. **LIDAR Configuration** (`settings_single_drone.json`):
   * 16-channel LIDAR sensor
   * 360° horizontal field of view
   * 30° vertical field of view
   * 10-meter range
   * 10,000 points per second

2. **Navigation Mechanism**:
   * Spiral pattern generation with dynamic radius
   * Real-time obstacle detection using LIDAR point cloud
   * Height adjustment based on obstacle proximity
   * Smooth trajectory planning

3. **Safety Features**:
   * Continuous LIDAR scanning
   * Obstacle detection in 3D space
   * Automatic height adjustment
   * Collision avoidance

### Swarm Navigation
The swarm system (`multi_drones_swarm.py`) implements coordinated movement of multiple drones:

1. **Swarm Configuration** (`settings_multi_drones_swarm.json`):
   * Six drones in hexagonal formation
   * Each drone equipped with 16-channel LIDAR
   * Vertical separation for collision prevention
   * Synchronized sensor configuration

2. **Swarm Mechanics**:
   * **Formation Types**:
     * Circle: Basic circular formation
     * Spiral: Dynamic spiral pattern
     * Wave: Complex wave pattern
     * Diamond: Diamond formation with scaling
     * Hexagon: Rotating hexagonal pattern
     * Cross: Dynamic cross formation

   * **Coordination System**:
     * Centralized swarm controller
     * Real-time position tracking
     * Formation maintenance
     * Collision avoidance between drones

3. **LIDAR Integration**:
   * Individual LIDAR sensors per drone
   * Point cloud processing for obstacle detection
   * Inter-drone distance monitoring
   * Formation maintenance using LIDAR data

4. **Safety Mechanisms**:
   * Minimum safety distance between drones
   * Dynamic height adjustment
   * Real-time collision risk assessment
   * Emergency maneuver capability

5. **Physics Considerations**:
   * Aerodynamic effects in formation
   * Wind resistance modeling
   * Drone interaction zones
   * Energy efficiency in formation

## Getting Started

### Prerequisites
* Unreal Engine 5.4
* Python environment (preferably Anaconda)
* [Colosseum AirSim Plugin](https://github.com/CodexLabsLLC/Colosseum) (We use Colosseum instead of Microsoft AirSim for UE5 compatibility)

### Installation Steps
1. Install Unreal Engine 5.4

2. Setting up Python Environment
   * Install Anaconda or Miniconda
   * Create and activate a new conda environment:
     ```bash
     conda create -n airsim python=3.10
     conda activate airsim
     ```

3. Installing the Python Client
   * Download the [PythonClient folder](https://github.com/CodexLabsLLC/Colosseum/tree/main/PythonClient) (We use Colosseum pythonclient instead of Microsoft AirSim python plugin for UE5 compatibility)
   * Navigate to the downloaded folder and run:
     ```bash
     python setup.py install
     ```
   This will install all necessary airsim dependencies in your conda environment.

4. AirSim Settings Configuration
   * Create a symbolic link between the project's settings file and AirSim's settings location:
     ```bash
     # For Windows (Run PowerShell as Administrator)
     New-Item -ItemType SymbolicLink -Path "C:\Users\<username>\OneDrive\Documents\AirSim\settings.json" -Target "<BlocksV2 project location>\AiClient\settings.json"
     ```
   * This creates a live link between the files, so any changes to `AiClient/settings.json` will automatically update the AirSim settings
   * The settings file contains drone configurations, sensor setups, and other simulation parameters

### Running the Project
1. Start the project from the UE5 editor (ASSETSVILLE demonstration map)
2. Run the Python aiclient script:
   ```bash
   # For single drone navigation
   python single_drone_navigation.py
   
   # For swarm navigation
   python multi_drones_swarm.py
   ```
3. The drone(s) should take off, execute their movement patterns, and finally land.

### Optional: Compiling the Plugin from Source
If you prefer to build the plugin yourself instead of using the pre-built version:
1. Clone the Colosseum repository: `git clone https://github.com/CodexLabsLLC/Colosseum`
2. Initialize submodules: `git submodule update --recursive --init`
3. Run `build.cmd` from Visual Studio terminal going inside the folder and it should compile the plugin.
4. Navigate to `Unreal/Environments/BlocksV2`
5. Copy and bring out the BlocksV2 folder to your desired location
6. Open this UE project

## Flight Behavior
The drone performs the following sequence:
1. Takes off to initial height
2. Executes a descending spiral pattern
3. Continuously monitors for obstacles using LIDAR
4. Adjusts height when obstacles are detected
5. Lands safely after completing the flight duration

## Future Enhancements

### Visual Odometry Integration
1. **Feature Detection Improvements**:
   * Implement ORB-SLAM3 for more robust feature tracking
   * Add loop closure detection for drift correction
   * Enhance feature matching with deep learning models
   * Implement real-time feature tracking optimization

2. **Sensor Fusion**:
   * Combine LIDAR and visual odometry data
   * Use LIDAR for short-range precision (0-5m)
   * Use visual odometry for long-range navigation (5m+)
   * Implement Kalman filtering for sensor fusion

3. **Use Case Optimization**:
   * **LIDAR Preferred When**:
     * High-precision short-range measurements needed
     * Operating in low-light conditions
     * Real-time obstacle avoidance required
     * Maintaining precise formation distances
     * Operating in featureless environments

   * **Visual Odometry Preferred When**:
     * Long-range navigation required
     * Rich visual features available
     * Energy efficiency is critical
     * Global positioning needed
     * Cross-drone recognition required

4. **Swarm Intelligence**:
   * Implement distributed visual odometry
   * Share feature maps between drones
   * Collaborative loop closure detection
   * Cross-drone feature matching
   * Swarm-wide pose graph optimization

5. **Performance Optimization**:
   * GPU-accelerated feature detection
   * Parallel processing for multiple drones
   * Efficient feature matching algorithms
   * Real-time pose estimation
   * Memory-efficient map representation

6. **Reliability Improvements**:
   * Robust failure detection
   * Automatic sensor switching
   * Degraded mode operation
   * Recovery from tracking loss
   * Backup navigation strategies

7. **Energy Efficiency**:
   * Adaptive sensor usage based on conditions
   * Dynamic feature detection density
   * Power-aware processing
   * Sleep mode for inactive sensors
   * Energy-efficient formation patterns

8. **Formation Control**:
   * Visual-based formation maintenance
   * Cross-drone visual tracking
   * Dynamic formation adaptation
   * Collision-free path planning
   * Formation reconfiguration

These enhancements aim to create a robust, efficient, and intelligent drone navigation system that can adapt to various environmental conditions and operational requirements.

