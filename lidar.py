import cv2
import numpy as np
import time
import math
from threading import Event
from windows_capture import WindowsCapture, Frame, InternalCaptureControl

def calculate_car_position(width, height, scaling_factor):
    return math.floor(width // 2), math.floor((height // 2) + 200 * scaling_factor)

def draw_lidar(frame, width, height, num_rays=20):
    """Simulates LIDAR and returns distances."""
    frame_original = frame.copy()
    scaling_factor = (height / 1080)
    cx, cy = calculate_car_position(width, height, scaling_factor)
    distances = []  # Store distance for each ray
    # max length of a ray assuming it starts at the bottom center and ends up in either top corner
    max_ray_length = math.ceil(math.sqrt((width / 2)**2 + height**2))

    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, max_ray_length, 1):
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            if frame_original[y,x][0] < 85 or frame_original[y,x][1] < 85 or frame_original[y,x][2] < 70:
                break

            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)  # Draw LIDAR point in RED
        distances.append(i / max_ray_length)
    return frame, distances

def calculate_lidar(frame, width, height, num_rays):
    """Calculate lidar without displaying anything for a significant performance improvement"""
    scaling_factor = (height / 1080)
    cx, cy = calculate_car_position(width, height, scaling_factor)
    distances = []  # Store distance for each ray
    # max length of a ray assuming it starts at the bottom center and ends up in either top corner
    max_ray_length = math.ceil(math.sqrt((width / 2)**2 + height**2))

    for angle in np.linspace(np.pi, 2 * np.pi, num_rays):
        dx, dy = np.cos(angle), np.sin(angle)
        for i in range(1, max_ray_length, 1):
            x, y = int(cx + dx * i), int(cy + dy * i)
            if x >= width or y >= height or x < 0 or y < 0:
                break

            if frame[y,x][0] < 85 or frame[y,x][1] < 85 or frame[y,x][2] < 70:
                break

        distances.append(i / max_ray_length)
    return distances

def main():
    frame_ready = Event()
    last_frame: dict[str, Frame] = {}
    
    capture = WindowsCapture(
        cursor_capture=False,
        draw_border=True,
        monitor_index=None,
        window_name='Trackmania',
    )

    @capture.event
    def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
        # global last_frame
        last_frame['value'] = frame
        # last_frame = frame
        frame_ready.set()

    @capture.event
    def on_closed():
        pass

    capture.start_free_threaded()

    frames = 0
    start = time.time()
    while True:
        frames += 1

        frame_ready.wait()
        frame_ready.clear()

        frame = last_frame['value']

        frame_data = cv2.cvtColor(frame.frame_buffer, cv2.COLOR_BGRA2BGR)
        height, width = frame.height, frame.width

        lidar_overlay, lidar_distances = draw_lidar(frame_data, width, height, 20)

        # Print the distances array
        print("LIDAR Distances:", lidar_distances)

        cv2.imshow("Trackmania LIDAR", lidar_overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # lidar_distances = calculate_lidar(frame_data, width, height, 20)
        # print("LIDAR Distances:", lidar_distances)

        if frames % 50 == 0:
            print(f'FPS: {frames / (time.time() - start)}')
            start = time.time()
            frames = 0

    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
