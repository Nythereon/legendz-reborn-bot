from mcstatus import JavaServer

from utils.logger import logger


def get_minecraft(server):

    try:
        status = JavaServer(server.public_ip, server.port).status() # Ping query server

        server.error = None
        server.version = status.version.name
        server.player_count = status.players.online
        server.max_players = status.players.max
        server.motd = status.description

    except Exception as error:
        logger('minecraft_query', str(error))
        server.error = str(error)