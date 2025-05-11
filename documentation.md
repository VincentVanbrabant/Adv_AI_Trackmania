# **Project Documentation: Advanced AI for Trackmania**

This project integrates AI with the Trackmania game using real-time gym environments, LiDAR simulation, and reinforcement learning. Below is a detailed explanation of each file in the project, based on its functionality and role in the system.

---

## **1. `TMDataAPIPlugin/main.as`**

This file is a server-side plugin for Trackmania, written in AngelScript. It streams real-time game data to a client over a socket connection.

### **Purpose**:

- Sends game data such as:
  - Current checkpoint (`CP`).
  - Time elapsed since the start of the race.
  - Speed, gear, and RPM of the car.
  - Distance to the next checkpoint.
  - Direction and position deltas relative to the next checkpoint.
- Acts as the data source for the AI system.

### **How It Works**:

- Listens for incoming connections on `127.0.0.1:9000`.
- Continuously streams data to connected clients using the `Send` function.
- Handles disconnections gracefully and resets the server when needed.

---

## **2. `trackmania_api.py`**

This file parses the raw data sent by the `TMDataAPIPlugin` into a structured format that can be used by the AI system.

### **Purpose**:

- Converts the binary data received from the Trackmania plugin into meaningful attributes such as:
  - Checkpoints passed (`cp`).
  - Current race time (`time`).
  - Speed, gear, RPM, and distance traveled.
  - Distance and direction to the next checkpoint.

### **Key Class**:

- **`TrackmaniaAPIData`**:
  - Parses the raw byte stream using the `struct` module.
  - Provides attributes like `cp`, `speed`, `rpm`, and `distance_to_cp` for easy access.

---

## **3. `interface.py`**

This file implements the `RealTimeGymInterface` class from the `rtgym` library, allowing the AI model to interact with the Trackmania game.

### **Purpose**:

- Acts as the bridge between the AI model and the game.
- Sends control inputs (e.g., throttle, brake, steering) to the game.
- Receives observations from the game, including:
  - Data parsed by `trackmania_api.py` (e.g., speed, gear, RPM).
  - LiDAR data calculated from screen captures.

### **Key Features**:

- **Frame Capture**:
  - Uses `WindowsCapture` to capture real-time frames of the game window.
  - Processes these frames to calculate LiDAR distances.
- **Control Input**:
  - Sends inputs to the game using the `vgamepad` library, simulating a virtual Xbox 360 controller.
- **Observation Space**:
  - Combines LiDAR data and Trackmania API data into a structured observation space for the AI model.
- **Reward Calculation**:
  - Uses `calculate_reward` from `reward.py` to compute rewards based on checkpoints passed and distance to the next checkpoint.

---

## **4. `lidar.py`**

This file simulates a LiDAR-inspired system for detecting track boundaries based on screen captures.

### **Purpose**:

- Provides spatial awareness to the AI by simulating virtual sensors that cast rays outward from the car.
- Measures the distance to track boundaries and returns these values as structured data.

### **Key Functions**:

- **`draw_lidar`**:
  - Simulates LiDAR by casting rays outward and visualizing the detected boundaries on the game frame.
  - Returns both the processed frame and the calculated distances.
- **`calculate_lidar`**:
  - Optimized version of LiDAR simulation without visualization for better performance.
- **`main()`**:
  - Captures frames from the game, processes them to simulate LiDAR, and displays the results in real time.

---

## **5. `reward.py`**

This file calculates the reward for the AI agent based on the game data.

### **Purpose**:

- Encourages the AI to pass checkpoints quickly and penalizes it for deviating from the optimal path.

### **Key Function**:

- **`calculate_reward`**:
  - Computes the reward using the formula:
    ```python
    reward = (api_data.cp * 300 - api_data.distance_to_cp + 90) / 100
    ```
  - Rewards the agent for passing checkpoints and getting closer to the next checkpoint.

---

## **6. [configuration.py](http://_vscodecontentref_/0)**

This file generates a configuration for the Trackmania environment.

### **Purpose**:

- Defines parameters for the environment, such as:
  - `steps_per_second`: How many times per second the AI should send an input.
  - `episode_duration`: How long each episode should last.

### **Key Class**:

- **`TrackmaniaConfiguration`**:
  - Generates a configuration dictionary compatible with the [rtgym](http://_vscodecontentref_/1) library.
  - Integrates the [TrackmaniaInterface](http://_vscodecontentref_/2) into the environment.

---

## **7. [main.py](http://_vscodecontentref_/3)**

This file brings all the components together and serves as the entry point for training and running the AI model.

### **Purpose**:

- Creates a gymnasium environment using the configuration from [configuration.py](http://_vscodecontentref_/4).
- Loads a pre-trained Soft Actor-Critic (SAC) model from `stable-baselines3`.
- Provides functions to train and run the model.

### **Key Functions**:

- **`train(time_between_saves)`**:
  - Trains the SAC model and periodically saves checkpoints.
- **`run()`**:
  - Runs the trained model in the environment to control the car.

---

## **8. `info.toml`**

This file provides metadata for the Trackmania Data API plugin.

### **Purpose**:

- Specifies the plugin name (`TM Data API`) and its dependencies (e.g., `PlayerState`).

---

## **9. [requirements.txt](http://_vscodecontentref_/5)**

This file lists the Python dependencies required for the project.

### **Dependencies**:

- [numpy](http://_vscodecontentref_/6): For numerical computations.
- `opencv-python`: For image processing and LiDAR visualization.
- [rtgym](http://_vscodecontentref_/7): For real-time gym environment integration.
- `stable-baselines3`: For reinforcement learning (SAC implementation).
- [vgamepad](http://_vscodecontentref_/8): For sending gamepad inputs to Trackmania.
- `windows-capture`: For capturing game frames.

---

## **10. `AI-test.Map.Gbx`**

This file is a placeholder for a Trackmania map used for testing the AI agent.

### **Purpose**:

- Contains the map data in `.Gbx` format.
- Used as the environment for training and testing the AI.

---

## **11. [.gitignore](http://_vscodecontentref_/9)**

This file specifies files and directories to be ignored by Git.

### **Ignored Items**:

- `__pycache__`: Python bytecode cache.
- [venv](http://_vscodecontentref_/10): Virtual environment directory.

---

## **How the Files Work Together**

### **Game Data Collection**:

- The [TMDataAPIPlugin](http://_vscodecontentref_/11) streams real-time game data to the client (`interface.py`).
- The [trackmania_api.py](http://_vscodecontentref_/12) file parses this data for use in the environment.

### **Environment Setup**:

- The [interface.py](http://_vscodecontentref_/13) file integrates the game with the [rtgym](http://_vscodecontentref_/14) framework.
- The [configuration.py](http://_vscodecontentref_/15) file configures the environment parameters.

### **AI Training and Execution**:

- The [main.py](http://_vscodecontentref_/16) file trains and runs the SAC agent using the environment.
- The [lidar.py](http://_vscodecontentref_/17) file provides LiDAR-based observations for the agent.

### **Dependencies**:

- The [requirements.txt](http://_vscodecontentref_/18) file ensures all necessary libraries are installed.
