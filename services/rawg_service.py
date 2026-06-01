import requests
import os

def get_image(game_name):
    url = 'https://api.rawg.io/api/games'
    API_KEY = os.getenv('RAWG_KEY')

    params = {
        'key': API_KEY,
        'search': game_name,
        'page_size': 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        game_image = data['results'][0]['background_image']
    except IndexError:
        print('No game image')
    else:
        return game_image