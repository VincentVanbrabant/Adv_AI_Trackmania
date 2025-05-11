from trackmania_api import TrackmaniaAPIData

def calculate_reward(api_data: TrackmaniaAPIData):
    return (api_data.cp * 300 - api_data.distance_to_cp + 90) / 100
