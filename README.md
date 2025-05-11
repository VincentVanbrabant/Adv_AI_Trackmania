# **Advanced AI for Trackmania**

This project integrates AI with the Trackmania game using real-time gym environments, LiDAR simulation, and reinforcement learning. The AI agent is trained using a Soft Actor-Critic (SAC) model to autonomously navigate tracks in the game.

---

## **Setup**

Follow these steps to set up the project and run the AI:

### **1. Install Dependencies**

1. **Install Python Dependencies**:

   - Ensure you have Python 3.8 or later installed.
   - Install the required Python libraries by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Install Trackmania**:

   - Download and install Trackmania from one of the following platforms:
     - [Steam](https://store.steampowered.com/)
     - [Ubisoft Store](https://store.ubi.com/)
     - [Epic Games Store](https://store.epicgames.com/)

3. **Install OpenPlanet**:

   - Download OpenPlanet from [https://openplanet.dev/](https://openplanet.dev/).
   - During installation, **change the destination folder** to the folder where Trackmania is installed.
   - Complete the installation process.

4. **Install the TMDataAPIPlugin**:

   - Copy the `TMDataAPIPlugin` folder from this repository to:
     ```
     C:\Users\<your-username>\OpenplanetNext\Plugins
     ```
     Replace `<your-username>` with your Windows username.

5. **Install the PlayerState Plugin**:
   - Start Trackmania.
   - If you don’t see the OpenPlanet bar in the top-left corner, press `F3`.
   - Go to **Plugin Manager** > **Open Manager** > **Search**.
   - Search for `PlayerState` and install the **PlayerState Info** plugin.

---

### **2. Configure Trackmania**

1. **Assign a Key to Camera 3**:

   - Open Trackmania.
   - Go to **Settings** > **Controls**.
   - Assign a key to **Camera 3** (e.g., `C`).

2. **Enable Developer Mode in OpenPlanet**:

   - Start Trackmania.
   - If you don’t see the OpenPlanet bar in the top-left corner, press `F3`.
   - Click **OpenPlanet** in the top-left corner > **Signature Mode** > **Developer**.
   - You will need to do this every time you start the game.

3. **Switch to Windowed Mode**:

   - If the game is in fullscreen mode, press `Alt + Enter` to switch to windowed mode.

4. **Set the Camera to First-Person View**:
   - Open a map (e.g., [AI-test.Map.Gbx](http://_vscodecontentref_/1)) by double-clicking on it.
   - Press the key assigned to **Camera 3** (step 1) until the camera is in first-person perspective and does not show the car.

---

### **3. Run the AI**

1. **Start Trackmania**:

   - Launch Trackmania.
   - When the game shows a logo, click the left mouse button a few times until you see a screen that says **Connecting...**.
   - Wait for the game to load.

2. **Run the AI**:
   - Open a terminal in the project directory.
   - Run the following command:
     ```bash
     python main.py
     ```
   - The AI will start controlling the car in the game.

---

## **Project Overview**

### **Purpose**

This project aims to train an AI agent to autonomously navigate tracks in Trackmania using reinforcement learning. The AI uses a LiDAR-inspired system to perceive its environment and a Soft Actor-Critic (SAC) model for decision-making.

### **Key Features**

- **Real-Time Interaction**: The AI interacts with the game in real time using the `rtgym` library.
- **LiDAR Simulation**: A custom LiDAR system provides spatial awareness by simulating virtual sensors.
- **Reinforcement Learning**: The AI is trained using the SAC algorithm from `stable-baselines3`.

---

## **File Descriptions**

### **1. [main.as](http://_vscodecontentref_/2)**

A server-side plugin for Trackmania that streams real-time game data to a client over a socket connection.

### **2. [trackmania_api.py](http://_vscodecontentref_/3)**

Parses raw data from the [TMDataAPIPlugin](http://_vscodecontentref_/4) into structured attributes (e.g., speed, checkpoints, distance to the next checkpoint).

### **3. [interface.py](http://_vscodecontentref_/5)**

Implements the `RealTimeGymInterface` class, allowing the AI to interact with the game by sending inputs and receiving observations.

### **4. [lidar.py](http://_vscodecontentref_/6)**

Simulates a LiDAR-inspired system to detect track boundaries based on screen captures.

### **5. [reward.py](http://_vscodecontentref_/7)**

Calculates rewards for the AI agent based on game data (e.g., checkpoints passed, distance to the next checkpoint).

### **6. [configuration.py](http://_vscodecontentref_/8)**

Generates a configuration for the Trackmania environment, defining parameters like `steps_per_second` and `episode_duration`.

### **7. [main.py](http://_vscodecontentref_/9)**

The entry point for training and running the AI model. It creates the environment, loads the SAC model, and provides functions to train and run the model.

### **8. `info.toml`**

Metadata for the Trackmania Data API plugin.

### **9. [requirements.txt](http://_vscodecontentref_/10)**

Lists the Python dependencies required for the project.

### **10. `AI-test.Map.Gbx`**

A Trackmania map used for testing the AI agent.

### **11. [.gitignore](http://_vscodecontentref_/11)**

Specifies files and directories to be ignored by Git (e.g., `__pycache__`, [venv](http://_vscodecontentref_/12)).

---

## **How the Files Work Together**

### **Game Data Collection**:

- The [TMDataAPIPlugin](http://_vscodecontentref_/13) streams real-time game data to the client (`interface.py`).
- The [trackmania_api.py](http://_vscodecontentref_/14) file parses this data for use in the environment.

### **Environment Setup**:

- The [interface.py](http://_vscodecontentref_/15) file integrates the game with the `rtgym` framework.
- The [configuration.py](http://_vscodecontentref_/16) file configures the environment parameters.

### **AI Training and Execution**:

- The [main.py](http://_vscodecontentref_/17) file trains and runs the SAC agent using the environment.
- The [lidar.py](http://_vscodecontentref_/18) file provides LiDAR-based observations for the agent.

### **Dependencies**:

- The [requirements.txt](http://_vscodecontentref_/19) file ensures all necessary libraries are installed.

---

## **Contributors**

- **Sam Verhaegen**:
  - Contributed to the LiDAR logic and screen capture implementation.
  - Took the lead on the machine learning component and proposed improvements to system performance.
- **Vincent Vanbrabant**:
  - Researched unfamiliar libraries and built the foundation of the LiDAR system.
  - Actively participated in debugging and design decisions and helped evaluate alternative approaches throughout the project.
- **GenAI**:
  - Used selectively to determine which libraries best suited our needs and to troubleshoot specific challenges in the LiDAR setup.
