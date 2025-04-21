# Adv_AI_Trackmania

This project integrates AI with the Trackmania game using real-time gym environments and LiDAR simulation.

## File Descriptions

### `api.py`

This file establishes a client connection to the Trackmania Data API server. It receives checkpoint and time data from the server and prints it to the console.

- **Key Features:**
  - Connects to the server at `127.0.0.1:9000`.
  - Continuously receives checkpoint and time data.
  - Handles graceful shutdown on a keyboard interrupt.

---

### `main.py`

This file sets up a real-time gym environment for Trackmania using the `rtgym` library.

- **Key Features:**
  - Configures the `TrackmaniaInterface` for the gym environment.
  - Runs a loop where an AI model (placeholder) interacts with the environment by taking actions and receiving observations, rewards, and termination signals.

---

### `lidar.py`

This file simulates and visualizes LiDAR data in the Trackmania game.

- **Key Features:**
  - **`draw_lidar`**: Simulates LiDAR by casting rays outward and visualizing them on the game frame.
  - **`calculate_lidar`**: Optimized version of LiDAR simulation without visualization for better performance.
  - **`main`**: Captures frames from Trackmania, processes them to simulate LiDAR, and displays the results in a window.

---

### `interface.py`

This file defines the `TrackmaniaInterface` class, which integrates the Trackmania game with the `rtgym` framework. It handles game input, frame capture, and LiDAR calculations.

- **Key Features:**
  - **`TrackmaniaInterface`**:
    - Captures frames from the game using `WindowsCapture`.
    - Sends control inputs to the game using `vgamepad`.
    - Computes LiDAR distances and provides observations to the gym environment.
  - **`calculate_reward`**: Computes rewards based on checkpoints passed and time taken.

---

## How to Run

1. Start the Trackmania game.
2. Run the `api.py` file to connect to the Trackmania Data API server.
3. Use `main.py` to start the real-time gym environment.
4. Optionally, use `lidar.py` to visualize LiDAR data in the game.

---

## Dependencies

- Python 3.x
- OpenCV
- NumPy
- `rtgym`
- `vgamepad`
- Trackmania Data API Plugin
