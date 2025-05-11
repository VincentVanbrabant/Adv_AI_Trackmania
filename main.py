import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import SAC
from configuration import TrackmaniaConfiguration
from datetime import datetime

steps_per_second = 25
episode_duration = 30

env = gym.make('real-time-gym-v1', config = TrackmaniaConfiguration.config(steps_per_second, episode_duration), disable_env_checker=True)
env = FlattenObservation(env)

model = SAC.load('sac_trackmania', env)

def train(time_between_saves):
    while True:
        try:
            model.learn(total_timesteps=time_between_saves * steps_per_second, log_interval=None)
            model.save(f'{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}-sac_trackmania')
        except KeyboardInterrupt:
            break

def run():
    obs, _info = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, terminated, truncated, _info = env.step(action)
        if terminated or truncated:
            obs, _info = env.reset()

run()
