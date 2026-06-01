import json

from mcstatus import JavaServer

def get_minecraft(server):
    # Get Minecraft query
    try:
        status = JavaServer(server.public_ip, server.port).status() # Ping query server

        server.version = status.version.name
        server.player_count = status.players.online
        server.max_players = status.players.max
        server.motd = status.description

    except Exception as error:
        server.error = str(error)