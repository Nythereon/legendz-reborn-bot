import requests
import os
from utils.logger import logger

def get_image(game_name):
    url = 'https://api.rawg.io/api/games'
    API_KEY = os.getenv('RAWG_KEY')

    params = {
        'key': API_KEY,
        'search': game_name,
        'page_size': 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        game_image = data['results'][0]['background_image']
    except Exception as error:
        logger('rawg_service', str(error))
        return None
    else:
        return game_image