import requests
import json
from mcstatus import JavaServer
from steam import SteamQuery
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://panel.legendzreborn.com/api/"
APP_KEY = os.getenv("APP_KEY")
CLIENT_KEY = os.getenv("CLIENT_KEY")

def get_servers(url):
    app_url = url+'application/servers?include=egg'

    headers = {
        "Authorization": f"Bearer {APP_KEY}",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }

    response = requests.get(app_url, headers=headers)
    server_data = response.json()

    server_info = {
        'server_count': 0,
        'servers': {}
    }

    for server in server_data['data']:
        attributes = server['attributes']
        environment = attributes['container']['environment']

        server_info['server_count'] +=1
        server_dict = {
            'server_name': attributes['name'],
            'game_name': server['attributes']['relationships']['egg']['attributes']['name'],
            # 'identifier': server['attributes']['identifier'],
            'nest': server['attributes']['nest'],
            'egg': server['attributes']['egg']
        }

        if 'QUERY_PORT' in environment:
            server_dict['query_port'] = environment['QUERY_PORT']

        server_info['servers'][attributes['identifier']] = server_dict

    return server_info

def get_minecraft(dictionary: dict, identifier, current_state, uptime, ip, port ):
    # Create server object for Minecraft
    server = JavaServer(ip, port)

    # Ping query server
    try:
        status = server.status()

        dictionary['servers'][identifier].update({
            # 'game_name': server_game,
            # 'server_name': server_name,
            'current_status': current_state,
            'uptime': uptime,
            'ip_address': ip,
            'port': port,
            'server_version': status.version.name,
            'players_online': status.players.online,
            'max_players': status.players.max,
            'MOTD': status.description
        })

    except Exception as error:
        dictionary['servers'][identifier].update({
            'error': str(error)
        })

def get_other_servers(dictionary: dict, identifier, server_game, server_name, current_state, uptime, ip, port):
    server = SteamQuery(ip, port)
    return_dictionary = server.query_server_info()
    # print(json.dumps(return_dictionary, indent=4))

def real_print(url):
    client_url = url + 'client/'
    server_info = get_servers(url)

    headers = {
        "Authorization": f"Bearer {CLIENT_KEY}",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }

    response = requests.get(client_url, headers=headers)
    data = response.json()

    for server in data['data']:

        identifier = server['attributes']['identifier']
        server_name = server['attributes']['name']
        server_game = server['attributes']['relationships']['allocations']['data'][0]['attributes']['ip_alias']
        ip = server['attributes']['relationships']['allocations']['data'][0]['attributes']['ip']
        port = server['attributes']['relationships']['allocations']['data'][0]['attributes']['port']

        server_url = url + f'client/servers/{identifier}/resources'
        next_response = requests.get(server_url, headers=headers)
        next_data = next_response.json()
        current_state = next_data['attributes']['current_state']
        uptime = next_data['attributes']['resources']['uptime']



        if server_info['servers'][identifier]['game_name'] == 'Paper':
            get_minecraft(server_info, identifier, current_state, uptime, ip, port)
        else:
            get_other_servers(server_info, identifier, server_game, server_name, current_state, uptime, ip, 27017)

        # print(json.dumps(server, indent=4))
    print(json.dumps(server_info, indent=4))

print('******** SERVER INFO ********')
real_print(URL)