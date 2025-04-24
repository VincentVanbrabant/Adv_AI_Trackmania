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

from trackmania_api import TrackmaniaAPIData

def calculate_reward(api_data: TrackmaniaAPIData):
    # TODO
    return api_data.cp * 300 - api_data.distance_to_cp

def calculate_car_position(width, height, scaling_factor):
    return math.floor(width // 2), math.floor((height // 2) + 200 * scaling_factor)

def calculate_lidar(frame, width, height, num_rays):
    scaling_factor = (height / 1080)
    cx, cy = calculate_car_position(width, height, scaling_factor)
    distances = []
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
            cursor_capture=False,
            draw_border=True,
            monitor_index=None,
            window_name='Trackmania',
        )

        @capture.event
        def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
            self.last_frame = frame
            # if self.frame_ready.is_set():
            #     print('unused frame')
            # else:
            #     print('used frame')
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
            self.gamepad.left_joystick_float((control[2] - 0.5) * 2.0, 0.0)
            self.gamepad.update()

    def _get_lidar(self):
        self.frame_ready.wait()
        self.frame_ready.clear()

        frame = self.last_frame

        frame_data = cv2.cvtColor(frame.frame_buffer, cv2.COLOR_BGRA2BGR)
        height, width = frame.height, frame.width

        return calculate_lidar(frame_data, width, height, self.num_rays)

    def _get_obs(self, api_data: TrackmaniaAPIData):
        return [self._get_lidar(), api_data.speed, api_data.gear, api_data.rpm]

    def reset(self, seed=None, options=None):
        self.gamepad.reset()
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()

        while True:
            response = self.client.recv(1024)
            api_data = TrackmaniaAPIData(response)
            if api_data.cp == 0:
                break

        self.start = time.time()
        self.steps = 0

        return self._get_obs(api_data), {}

    # def wait(self):
    #     pass

    def get_obs_rew_terminated_info(self):
        response = self.client.recv(1024)
        api_data = TrackmaniaAPIData(response)

        self.steps += 1
        if self.steps % 25 == 0:
            print(f'Steps per second: {self.steps/(time.time()-self.start):2f}')
            print(f'Reward: {calculate_reward(api_data)}, {api_data.cp}, {api_data.distance_to_cp}')
            self.start = time.time()
            self.steps = 0

        return self._get_obs(api_data), calculate_reward(api_data), api_data.cp == 4294967295, {}

    def get_observation_space(self):
        lidar = spaces.Box(low=0.0, high=1.0, shape=(self.num_rays,))
        speed = spaces.Box(low=0.0, high=1000.0, shape=(1,))
        gear = spaces.Box(low=1.0, high=5.0, shape=(1,))
        rpm = spaces.Box(low=0.0, high=11000.0, shape=(1,))
        return spaces.Tuple((lidar, speed, gear, rpm))

    def get_action_space(self):
        return spaces.Box(low=0.0, high=1.0, shape=(3,))

    def get_default_action(self):
        return np.array([0.0, 0.0, 0.0], dtype='float32')

    # def render(self):
    #     pass
