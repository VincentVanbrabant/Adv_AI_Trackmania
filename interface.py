from rtgym import RealTimeGymInterface
from gymnasium import spaces
from threading import Event
from windows_capture import WindowsCapture, Frame, InternalCaptureControl
import vgamepad as vg
import numpy as np
import socket
import cv2
import time
import math

def calculate_reward(cp, time):
    # TODO
    if cp == 4294967295: return 100 / time
    if time == 0.0: return 0
    return cp / time

def calculate_car_position(width, height, scaling_factor):
    return math.floor(width // 2), math.floor((height // 2) + 200 * scaling_factor)

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

            if i < 175 * scaling_factor:
                continue

            if frame[y,x][0] < 85 or frame[y,x][1] < 85 or frame[y,x][2] < 70:
                break

        distances.append(i / max_ray_length)
    return distances

class TrackmaniaInterface(RealTimeGymInterface):
    def __init__(self, num_rays=20):
        self.gamepad = vg.VX360Gamepad()
        self.num_rays = num_rays

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9000))

        self.client = client

        self.frame_ready = Event()
        self.last_frame: Frame
        
        capture = WindowsCapture(
            cursor_capture=None,
            draw_border=None,
            monitor_index=None,
            window_name='Trackmania',
        )

        @capture.event
        def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
            self.last_frame = frame
            self.frame_ready.set()

        @capture.event
        def on_closed():
            pass

        capture.start_free_threaded()

        self.capture = capture

    def send_control(self, control):
        if control is not None:
            self.gamepad.right_trigger_float(control[0])
            self.gamepad.left_trigger_float(control[1])
            self.gamepad.left_joystick_float(control[2], 0.0)
            self.gamepad.update()

    def _get_obs(self):
        self.frame_ready.wait()
        self.frame_ready.clear()

        frame = self.last_frame

        frame_data = cv2.cvtColor(frame.frame_buffer, cv2.COLOR_BGRA2BGR)
        height, width = frame.height, frame.width

        return calculate_lidar(frame_data, width, height, self.num_rays)

    def reset(self, seed=None, options=None):
        self.gamepad.reset()
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

        self.client.recv(1024)
        time.sleep(0.1)

        while True:
            response = self.client.recv(1024)
            cp = int.from_bytes(response[-8:-4], byteorder='little', signed=False)
            if cp == 0:
                break

        return [self._get_obs()], {}

    # def wait(self):
    #     pass

    def get_obs_rew_terminated_info(self):
        response = self.client.recv(1024)
        cp, time = (
            int.from_bytes(response[-8:-4], byteorder='little', signed=False),
            int.from_bytes(response[-4:], byteorder='little', signed=False),
        )
        return [self._get_obs()], calculate_reward(cp, time), cp == 4294967295, {}

    def get_observation_space(self):
        lidar = spaces.Box(low=np.array([0.0] * self.num_rays, dtype='float32'), high=np.array([1.0] * self.num_rays, dtype='float32'), shape=(self.num_rays,))
        return spaces.Tuple((lidar,))

    def get_action_space(self):
        acceleration = spaces.Box(low=0.0, high=1.0, shape=(1,))
        braking = spaces.Box(low=0.0, high=1.0, shape=(1,))
        steering = spaces.Box(low=-0.5, high=0.5, shape=(1,))
        return spaces.Tuple((acceleration, braking, steering))

    def get_default_action(self):
        return np.array([0.0, 0.0, 0.0], dtype='float32')

    # def render(self):
    #     pass
