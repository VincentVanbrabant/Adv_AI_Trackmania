import cv2
import numpy as np
import mss

def detect_edges(frame):
    """Detects black edges using color filtering."""
    # Define the lower and upper bounds for black color in BGR
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([30, 30, 30])  # Adjust these values as needed

    # Create a mask for black pixels
    mask = cv2.inRange(frame, lower_black, upper_black)

    # Apply Canny edge detection on the mask
    edges = cv2.Canny(mask, 50, 150)
    return edges

def draw_lidar(frame, edges, car_position, num_rays=60):
    """Simulates LIDAR by casting rays outward and stopping at detected edges."""
    height, width = frame.shape[:2]
    cx, cy = car_position

    # Change the angle range to scan 180 degrees behind the car
    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):  # Scan from 180 to 360 degrees
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, 600, 5):  # Make the lines longer
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            # Add a vertical threshold to limit LIDAR's range
            if y < height // 3:  # Adjust height // 3 to set the threshold
                break

            if edges[y, x] > 0:
                break
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)  # Draw LIDAR point in RED
    return frame

def capture_screen():
    """Captures the screen and returns a BGR frame."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

while True:
    frame = capture_screen()
    height, width = frame.shape[:2] # get screen height and width
    edges = detect_edges(frame) # now detects black edges
    lidar_overlay = draw_lidar(frame, edges, (width // 2, (height // 2) + 50))  # Center and slightly lower
    cv2.imshow("Trackmania LIDAR", lidar_overlay)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()