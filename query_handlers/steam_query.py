from steam import SteamQuery
import json

def get_steam_servers(server):

    try:
        status = SteamQuery(server.public_ip, int(server.query_port))
        return_dictionary = status.query_server_info()

        server.map = return_dictionary['map']
        server.player_count = return_dictionary['players']
        server.max_players = return_dictionary['max_players']

    except Exception as error:
        server.error = str(error)

