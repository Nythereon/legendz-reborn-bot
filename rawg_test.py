import requests
import json
import webbrowser

url = 'https://api.rawg.io/api/games'
API_KEY = '430bf52ec9884f888b04d66b0c446935'


params = {
    'key': API_KEY,
    'search': "Legend of Zelda Twilight Princess",
    'page_size': 1
}

response = requests.get(url, params=params)

data = response.json()
game_image = data['results'][0]['background_image']
