import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import PPO
from interface import TrackmaniaInterface
from rtgym.envs.real_time_env import DEFAULT_CONFIG_DICT

# TODO
trackmania_config = DEFAULT_CONFIG_DICT
trackmania_config['interface'] = TrackmaniaInterface

env = gym.make('real-time-gym-v1', config=trackmania_config, disable_env_checker=True)
env = FlattenObservation(env)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo_trackmania")

model = PPO.load("ppo_trackmania")
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        env.reset()
