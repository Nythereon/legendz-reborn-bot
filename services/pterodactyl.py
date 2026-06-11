import requests
import os
from dotenv import load_dotenv
from game_handler import GAME_HANDLERS
from models.server_manager import ServerManager
from models.server_object import ServerObject
from utils.logger import logger

load_dotenv()


APP_KEY = os.getenv("APP_KEY")
CLIENT_KEY = os.getenv("CLIENT_KEY")


def make_request(url, header):

    for _ in range(3):
        try:
            response = requests.get(url=url, headers=header, timeout=10)
            data = response.json()
        except Exception as error:
            logger('pterodactyl_request', str(error))
            continue

        else:
            return data

    return None

def get_all_server_data(url, public_ip):

    client_headers = {
        "Authorization": f"Bearer {CLIENT_KEY}",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }

    app_headers = {
        "Authorization": f"Bearer {APP_KEY}",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }

    manager = ServerManager()

    try:
        client_info = get_client_data(url, client_headers, public_ip)
    except Exception as e:
        logger('get_client_data', str(e))
        return manager

    try:
        application_info = get_application_data(url, app_headers)
    except Exception as e:
        logger('get_application_data', str(e))
        return manager

    if not application_info:
        return manager

    for identifier, server_data in application_info.items():
        if "Eric's Palworld Server" in application_info[identifier]['server_name']:
            pass
        else:
            manager.servers[identifier] = {
                'server_name': server_data['server_name'],
                'game_type': server_data['game_name'],
                'egg': server_data['egg'],
                'nest': server_data['nest']
            }

    if not client_info:
        return manager

    required = [
        'ip',
        'port',
        'uptime',
        'public_ip',
        'current_state'
    ]

    for identifier, server_data in client_info.items():

        if identifier not in manager.servers:
            logger(
                'get_all_server_data',
                f'{identifier} missing from manager.servers'
            )
            continue

        if not all(key in server_data for key in required):
            logger(
                'get_all_server_data',
                f'Missing data for {identifier}: {server_data}'
            )
            continue

        manager.servers[identifier].update({
            'ip': server_data['ip'],
            'port': server_data['port'],
            'current_state': server_data['current_state'],
            'uptime': server_data['uptime'],
            'public_ip': server_data['public_ip'],
        })

        if 'query_port' in server_data:
            manager.servers[identifier]['query_port'] = server_data['query_port']

        if 'rcon' in server_data:
            manager.servers[identifier]['rcon'] = server_data['rcon']

    for identifier, server_data in manager.servers.items():
        server_identity = manager.servers[identifier]
        ip = server_identity['ip']

        server_name = server_identity['server_name']
        game_type = server_identity['game_type']
        egg = server_identity['egg']
        nest = server_identity['nest']
        current_state = server_identity['current_state']
        uptime = server_identity['uptime']
        public_ip = server_identity['public_ip']
        port = server_identity['port']


        server = ServerObject(ip=ip, port=port, identifier=identifier, server_name=server_name, game_type=game_type)
        server.egg = egg
        server.nest = nest
        server.public_ip = public_ip
        server.uptime = uptime
        server.current_state = current_state

        if 'query_port' in server_identity:
            server.query_port = server_identity['query_port']

        if 'rcon' in server_identity:
            server.rcon = server_identity['rcon']

        manager.servers[identifier] = server

        handler = GAME_HANDLERS.get(server.game_type)

        if handler:
            handler(server)

    return manager

def get_client_data(url, header, public_ip):
    client_info = {}

    client_url = url + 'client/'
    data = make_request(client_url, header)

    if data is None:
        return {}

    if 'data' not in data:
        logger('get_client_data', f'Unexpected response: {data}')
        return {}


    for server in data['data']:

        attributes = server['attributes']
        identifier = attributes['identifier']
        allocations = attributes['relationships']['allocations']['data']

        client_info[identifier] = {
            'ip': allocations[0]['attributes']['ip'],
            'server_name': attributes['name']
        }

        client_identity = client_info[identifier]

        resource_url = url + f'client/servers/{identifier}/resources'

        resource_data = make_request(resource_url, header)

        if resource_data is None:
            continue

        if 'attributes' in resource_data:
            current_state = resource_data['attributes']['current_state']
            uptime = resource_data['attributes']['resources']['uptime']

            client_info[identifier].update({
                'current_state': current_state,
                'uptime': uptime,
                'public_ip': public_ip
            })

        for allocation in allocations:
            attributes = allocation['attributes']

            if attributes['is_default']:
                client_identity['port'] = attributes['port']

            if 'query' in attributes['ip_alias'].lower():
                client_identity['query_port'] = attributes['port']

            if 'rcon' in attributes['ip_alias'].lower():
                client_identity['rcon'] = attributes['port']

    return client_info

def get_application_data(url, header):
    application_info = {}
    app_url = url + 'application/servers?include=egg'

    server_data = make_request(app_url, header)

    if server_data is None:
        return {}

    if 'data' not in server_data:
        logger('get_application_data', f'Unexpected Response {server_data}')
        return {}

    for server in server_data['data']:
        attributes = server['attributes']
        identifier = server['attributes']['identifier']

        application_info[identifier] = {
            'server_name': attributes['name'],
            'game_name': server['attributes']['relationships']['egg']['attributes']['name'],
            'nest': server['attributes']['nest'],
            'egg': server['attributes']['egg'],
        }

    return application_info