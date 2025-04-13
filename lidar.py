import cv2
import numpy as np
import time
from threading import Event
from windows_capture import WindowsCapture, Frame, InternalCaptureControl

def draw_lidar(frame, car_position, num_rays=20):
    """Simulates LIDAR and returns distances."""
    frame_original = frame.copy()
    height, width = frame.shape[:2]
    cx, cy = car_position
    distances = []  # Store distance for each ray

    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, 1000, 1):
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            if i < 175:
                continue

            if frame_original[y,x][0] < 85 or frame_original[y,x][1] < 85 or frame_original[y,x][2] < 70:
                break

            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)  # Draw LIDAR point in RED
        distances.append(i)
    return frame, distances

def calculate_lidar(frame, car_position, num_rays=20):
    """Calculate lidar without displaying anything for a significant performance improvement"""
    height, width = frame.shape[:2]
    cx, cy = car_position
    distances = []  # Store distance for each ray

    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, 1000, 1):
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            if i < 175:
                continue

            if frame[y,x][0] < 85 or frame[y,x][1] < 85 or frame[y,x][2] < 70:
                break

        distances.append(i)
    return distances

frame_ready = Event()
last_frame: Frame

capture = WindowsCapture(
    cursor_capture=None,
    draw_border=None,
    monitor_index=None,
    window_name='Trackmania',
)

@capture.event
def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
    global last_frame
    last_frame = frame
    frame_ready.set()

@capture.event
def on_closed():
    pass

def main():
    capture.start_free_threaded()

    frames = 0
    start = time.time()
    while True:
        frames += 1

        frame_ready.wait()
        frame_ready.clear()

        frame = cv2.cvtColor(last_frame.frame_buffer, cv2.COLOR_BGRA2BGR)
        height, width = last_frame.height, last_frame.width

        # lidar_overlay, lidar_distances = draw_lidar(frame, (width // 2, (height // 2) + 200))

        # Print the distances array
        # print("LIDAR Distances:", lidar_distances)

        # cv2.imshow("Trackmania LIDAR", lidar_overlay)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        lidar_distances = calculate_lidar(frame, (width // 2, (height // 2) + 200))
        # print("LIDAR Distances:", lidar_distances)

        if frames % 50 == 0:
            print(f'FPS: {frames / (time.time() - start)}')
            start = time.time()
            frames = 0

    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
