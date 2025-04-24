from rtgym.envs.real_time_env import DEFAULT_CONFIG_DICT

from interface import TrackmaniaInterface

class TrackmaniaConfiguration:
    def config(steps_per_second: float, episode_duration: float):
        trackmania_config = DEFAULT_CONFIG_DICT
        trackmania_config['interface'] = TrackmaniaInterface

        trackmania_config['time_step_duration'] = 1 / steps_per_second
        trackmania_config['start_obs_capture'] = 1 / steps_per_second

        trackmania_config['ep_max_length'] = episode_duration * steps_per_second
        
        return trackmania_config