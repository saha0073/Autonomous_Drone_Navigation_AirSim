# Cinematic Drone Navigation with AirSim

A dynamic drone navigation system that creates cinematic spiral flight patterns while incorporating real-time obstacle avoidance using LIDAR data in AirSim simulation environment.

## Demo
[![Watch the Demo on YouTube](https://img.youtube.com/vi/Szfl03-d1VI/0.jpg)](https://youtu.be/Szfl03-d1VI) 
▶️ *Click to watch the demo video on YouTube*

This project implements an autonomous drone control system that generates smooth, cinematic flight paths while maintaining safety through obstacle detection. The drone follows a descending spiral pattern while dynamically adjusting its trajectory based on LIDAR sensor data.

## Features
* Autonomous spiral flight pattern generation
* Real-time LIDAR-based obstacle detection and avoidance
* Smooth trajectory adjustments
* Configurable flight parameters
* Custom camera positioning for cinematic captures

## Technical Stack
* Simulation Environment: Unreal Engine 5 with Colosseum AirSim plugin
* Programming Language: Python
* Libraries: AirSim Python API
* Sensors: LIDAR (16-channel)

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
   * Download the [PythonClient folder](https://github.com/CodexLabsLLC/Colosseum/tree/main/PythonClient)
   * Navigate to the downloaded folder and run:
     ```bash
     python setup.py install
     ```
   This will install all necessary dependencies in your conda environment.

4. AirSim Settings Configuration
   * Copy `AiClient/settings.json` to `C:\Users\<username>\OneDrive\Documents\AirSim\`
   * This configuration file is essential for drone setup and sensor configurations

### Running the Project
1. Start the project from the UE5 editor (ASSETSVILLE demonstration map)
2. Run the Python script:
   ```bash
   python drone_navigation.py
   ```
3. The drone will:
   - Take off to initial height
   - Execute a rotating spiral pattern
   - Land automatically after completing the sequence

### Optional: Building the Plugin from Source
If you prefer to build the plugin yourself instead of using the pre-built version:
1. Clone the Colosseum repository: `git clone https://github.com/CodexLabsLLC/Colosseum`
2. Initialize submodules: `git submodule update --recursive --init`
3. Run `build.cmd` from Visual Studio terminal
4. Navigate to `unreal/environments/Blockv2`
5. Copy the Blockv2 folder to your desired location
6. Open this UE project

## Flight Behavior
The drone performs the following sequence:
1. Takes off to initial height
2. Executes a descending spiral pattern
3. Continuously monitors for obstacles using LIDAR
4. Adjusts height when obstacles are detected
5. Lands safely after completing the flight duration

## Future Enhancements
* Integration of advanced path-finding algorithms
* Implementation of deep learning for obstacle prediction
* Multi-modal vision systems for enhanced environment perception
* Support for multiple drone coordination
* Custom flight pattern generation

