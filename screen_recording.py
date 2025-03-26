import cv2
import numpy as np
import mss

def draw_lidar(frame, car_position, num_rays=20):
    """Simulates LIDAR by casting rays outward and stopping at detected edges."""
    height, width = frame.shape[:2]
    cx, cy = car_position

    # Change the angle range to scan 180 degrees behind the car
    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):  # Scan from 180 to 360 degrees
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, 1000, 3):  # Make the lines longer
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            # Don't check immediately around the car
            if i < 175:
                continue

            if frame[y,x][0] < 96 or frame[y,x][1] < 96 or frame[y,x][1] > 255 or frame[y,x][2] < 96:
                break
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)  # Draw LIDAR point in RED
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
    lidar_overlay = draw_lidar(frame, (width // 2, (height // 2) + 200))  # Center and slightly lower
    cv2.imshow("Trackmania LIDAR", lidar_overlay)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()