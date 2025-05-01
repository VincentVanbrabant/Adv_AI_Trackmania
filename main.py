import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import SAC
from configuration import TrackmaniaConfiguration
from datetime import datetime

steps_per_second = 25
episode_duration = 30
training_duration = 600 * steps_per_second

env = gym.make('real-time-gym-v1', config = TrackmaniaConfiguration.config(steps_per_second, episode_duration), disable_env_checker=True)
env = FlattenObservation(env)

model = SAC.load("sac_trackmania")

def train():
    for i in range(6):
        model.learn(total_timesteps=training_duration, log_interval=None)
        model.save(f"{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}-sac _trackmania")


def run():
    obs, _info = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            obs, _info = env.reset()

train()
