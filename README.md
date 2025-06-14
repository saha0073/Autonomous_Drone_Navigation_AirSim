# Autonommous Drone Navigation with AirSim inside Unreal Engine

A dynamic drone navigation system that creates cinematic flight patterns while incorporating real-time obstacle avoidance using LIDAR data. The system supports both individual drone navigation with spiral patterns and coordinated swarm movements with multiple drones, all implemented using AirSim simulation inside Unreal Engine environment.

## Demo

<a href="https://www.youtube.com/watch?v=Szfl03-d1VI">
  <img src="https://i.ytimg.com/vi/Szfl03-d1VI/mqdefault.jpg" alt="Watch the Spiral Pattern Demo" width="400"/>
</a>

▶️ *Click the image above to watch the single drone spiral pattern navigation demo*

<a href="https://www.youtube.com/watch?v=z0FzZgCPRPk">
  <img src="Recordings/swarm_drones_formation.png" alt="Watch the Swarm Demo" width="400"/>
</a>

▶️ *Click the image above to watch the multi-drone swarm coordination demo*

This project implements an autonomous drone control system that generates smooth, cinematic flight paths while maintaining safety through obstacle detection.

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

4. **Flight Behavior**:
   * Initial takeoff to -3 meters height
   * Descending spiral pattern with dynamic radius
   * Continuous LIDAR scanning for obstacles
   * Automatic height adjustment when obstacles detected
   * Smooth landing sequence
   * Total flight duration: 30 seconds
   * Angular speed: 0.5 radians per second
   * Height increment: 0.03 meters per step

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

5. **Flight Behavior**:
   * Synchronized takeoff of all drones
   * Dynamic formation transitions every 2π radians
   * Continuous formation maintenance
   * Real-time obstacle avoidance
   * Coordinated landing sequence
   * Total flight duration: 30 seconds
   * Formation radius: 5 meters
   * Angular speed: 0.5 radians per second
   * Safety distance: 2 meters between drones

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

## Future Enhancements

1. **Visual Odometry Integration**
   * Implement ORB-SLAM3 for improved feature detection and tracking
   * Add sensor fusion between LIDAR and visual odometry data

2. **Swarm Intelligence**
   * Implement distributed visual odometry for swarm coordination
   * Add collaborative feature detection between drones

3. **Performance Optimization**
   * GPU acceleration for visual odometry processing
   * Parallel processing for real-time feature matching

4. **Reliability Improvements**
   * Robust failure detection and automatic sensor switching
   * Enhanced error recovery mechanisms

5. **Formation Control**
   * Visual-based formation maintenance
   * Dynamic formation adaptation based on environment

The current visual odometry implementation (`visual_odometry.py`) provides:
* ORB feature detection and matching
* Real-time position estimation
* Multi-drone coordination support
* Thread-safe updates for swarm operations

These enhancements aim to create a robust, efficient, and intelligent drone navigation system that can adapt to various environmental conditions and operational requirements.

