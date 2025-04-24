import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3 import PPO
from configuration import TrackmaniaConfiguration

steps_per_second = 30
episod_duration = 20
training_duration = 900 * steps_per_second

env = gym.make('real-time-gym-v1', config = TrackmaniaConfiguration.config(steps_per_second, episod_duration), disable_env_checker=True)
env = FlattenObservation(env)

model = PPO("MlpPolicy", env, verbose=0)
model.learn(total_timesteps=training_duration, log_interval=None)
model.save("ppo_trackmania")

model = PPO.load("ppo_trackmania")
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs = env.reset()
