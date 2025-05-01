import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import PPO, SAC
from configuration import TrackmaniaConfiguration
import time
from datetime import datetime

steps_per_second = 25
episode_duration = 60
training_duration = 600 * steps_per_second

env = gym.make('real-time-gym-v1', config = TrackmaniaConfiguration.config(steps_per_second, episode_duration), disable_env_checker=True)
env = FlattenObservation(env)

# start = time.time()

# model = SAC("MlpPolicy", env, verbose=0) # , train_freq=(1, 'episode'), gradient_steps=-1, learning_starts=0

# for i in range(6):
#     model.learn(total_timesteps=training_duration, log_interval=None)
#     model.save(f"{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}-ppo_trackmania")

# import sys
# print(time.time() - start)
# sys.exit(0)

# import numpy as np
# def random_model():
#     return [np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0)]

model = SAC.load("sac_trackmania")
obs, _info = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, _info = env.reset()
