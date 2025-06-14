import airsim
import cv2
import numpy as np
import time
from typing import Tuple, List, Dict
import threading

class VisualOdometry:
    def __init__(self, client: airsim.MultirotorClient, drone_name: str):
        self.client = client
        self.drone_name = drone_name
        self.prev_image = None
        self.prev_keypoints = None
        self.prev_descriptors = None
        self.position = (0, 0, 0)
        self.velocity = (0, 0, 0)
        self.last_update_time = time.time()
        
        # Initialize ORB detector
        self.orb = cv2.ORB_create(
            nfeatures=1000,
            scaleFactor=1.2,
            nlevels=8,
            edgeThreshold=31
        )
        
        # Initialize feature matcher
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        print(f"Initialized Visual Odometry for {drone_name}")
    
    def get_camera_image(self) -> np.ndarray:
        """Get image from the drone's camera"""
        try:
            # Get image from AirSim
            image_response = self.client.simGetImages([
                airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)
            ], vehicle_name=self.drone_name)[0]
            
            # Convert to numpy array
            img1d = np.frombuffer(image_response.image_data_uint8, dtype=np.uint8)
            img = img1d.reshape(image_response.height, image_response.width, 3)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return gray
            
        except Exception as e:
            print(f"Error getting camera image for {self.drone_name}: {str(e)}")
            return None
    
    def detect_features(self, image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray]:
        """Detect features in the image using ORB"""
        try:
            keypoints, descriptors = self.orb.detectAndCompute(image, None)
            return keypoints, descriptors
        except Exception as e:
            print(f"Error detecting features for {self.drone_name}: {str(e)}")
            return [], None
    
    def match_features(self, desc1: np.ndarray, desc2: np.ndarray) -> List[cv2.DMatch]:
        """Match features between two images"""
        try:
            if desc1 is None or desc2 is None:
                return []
            matches = self.matcher.match(desc1, desc2)
            # Sort matches by distance
            matches = sorted(matches, key=lambda x: x.distance)
            return matches
        except Exception as e:
            print(f"Error matching features for {self.drone_name}: {str(e)}")
            return []
    
    def estimate_motion(self, matches: List[cv2.DMatch], 
                       kp1: List[cv2.KeyPoint], kp2: List[cv2.KeyPoint]) -> Tuple[float, float, float]:
        """Estimate motion from matched features"""
        try:
            if len(matches) < 8:
                return (0, 0, 0)
            
            # Get matched keypoints
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            
            # Calculate essential matrix
            E, mask = cv2.findEssentialMat(src_pts, dst_pts, focal=1.0, pp=(0., 0.))
            
            # Recover pose
            _, R, t, _ = cv2.recoverPose(E, src_pts, dst_pts)
            
            # Convert rotation matrix to euler angles
            angles = cv2.RQDecomp3x3(R)[0]
            
            return (t[0][0], t[1][0], t[2][0])
            
        except Exception as e:
            print(f"Error estimating motion for {self.drone_name}: {str(e)}")
            return (0, 0, 0)
    
    def update(self) -> Tuple[float, float, float]:
        """Update visual odometry estimate"""
        try:
            # Get current image
            current_image = self.get_camera_image()
            if current_image is None:
                return self.position
            
            # Detect features
            current_keypoints, current_descriptors = self.detect_features(current_image)
            
            if self.prev_image is not None:
                # Match features
                matches = self.match_features(self.prev_descriptors, current_descriptors)
                
                # Estimate motion
                motion = self.estimate_motion(matches, self.prev_keypoints, current_keypoints)
                
                # Update position
                dt = time.time() - self.last_update_time
                self.velocity = (
                    motion[0] / dt if dt > 0 else 0,
                    motion[1] / dt if dt > 0 else 0,
                    motion[2] / dt if dt > 0 else 0
                )
                
                self.position = (
                    self.position[0] + self.velocity[0] * dt,
                    self.position[1] + self.velocity[1] * dt,
                    self.position[2] + self.velocity[2] * dt
                )
            
            # Update previous frame
            self.prev_image = current_image
            self.prev_keypoints = current_keypoints
            self.prev_descriptors = current_descriptors
            self.last_update_time = time.time()
            
            return self.position
            
        except Exception as e:
            print(f"Error updating visual odometry for {self.drone_name}: {str(e)}")
            return self.position

class SwarmVisualOdometry:
    def __init__(self, client: airsim.MultirotorClient, drone_names: List[str]):
        self.client = client
        self.drone_names = drone_names
        self.odometry_instances: Dict[str, VisualOdometry] = {}
        self.positions: Dict[str, Tuple[float, float, float]] = {}
        self.running = False
        self.update_thread = None
        
        # Initialize visual odometry for each drone
        for drone_name in drone_names:
            self.odometry_instances[drone_name] = VisualOdometry(client, drone_name)
            self.positions[drone_name] = (0, 0, 0)
        
        print(f"Initialized Swarm Visual Odometry for drones: {drone_names}")
    
    def start(self):
        """Start visual odometry updates"""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.start()
        print("Started visual odometry updates")
    
    def stop(self):
        """Stop visual odometry updates"""
        self.running = False
        if self.update_thread:
            self.update_thread.join()
        print("Stopped visual odometry updates")
    
    def _update_loop(self):
        """Update loop for visual odometry"""
        while self.running:
            try:
                for drone_name in self.drone_names:
                    position = self.odometry_instances[drone_name].update()
                    self.positions[drone_name] = position
                    print(f"{drone_name} position: x={position[0]:.2f}, y={position[1]:.2f}, z={position[2]:.2f}")
                time.sleep(0.1)  # Update at 10 Hz
            except Exception as e:
                print(f"Error in visual odometry update loop: {str(e)}")
                time.sleep(1)
    
    def get_positions(self) -> Dict[str, Tuple[float, float, float]]:
        """Get current positions of all drones"""
        return self.positions.copy()
    
    def get_relative_positions(self) -> Dict[str, Dict[str, Tuple[float, float, float]]]:
        """Get relative positions between all drones"""
        relative_positions = {}
        for drone1 in self.drone_names:
            relative_positions[drone1] = {}
            for drone2 in self.drone_names:
                if drone1 != drone2:
                    pos1 = self.positions[drone1]
                    pos2 = self.positions[drone2]
                    relative_positions[drone1][drone2] = (
                        pos2[0] - pos1[0],
                        pos2[1] - pos1[1],
                        pos2[2] - pos1[2]
                    )
        return relative_positions

# Example usage:
if __name__ == "__main__":
    # Connect to AirSim
    client = airsim.MultirotorClient()
    client.confirmConnection()
    
    # Initialize swarm visual odometry
    drone_names = ["Drone1", "Drone2", "Drone3", "Drone4", "Drone5", "Drone6"]
    swarm_vo = SwarmVisualOdometry(client, drone_names)
    
    try:
        # Start visual odometry
        swarm_vo.start()
        
        # Run for 30 seconds
        time.sleep(30)
        
    finally:
        # Stop visual odometry
        swarm_vo.stop() 