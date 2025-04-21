import gymnasium
from interface import TrackmaniaInterface
from rtgym.envs.real_time_env import DEFAULT_CONFIG_DICT

# TODO
trackmania_config = DEFAULT_CONFIG_DICT
trackmania_config['interface'] = TrackmaniaInterface

env = gymnasium.make('real-time-gym-v1', config=trackmania_config, disable_env_checker=True)

def model():
	# TODO
	return [1.0, 0.0, 0.0]

obs, info = env.reset()
while True:
	act = model()
	obs, rew, terminated, truncated, info = env.step(act)
	if terminated or truncated:
		env.reset()
