from utils.logger import logger

def reset_mysql(connection):

    cursor = connection.cursor()  # Create cursor object

    # SQL Query
    query = """
    UPDATE servers
    SET player_count = 0
    """

    cursor.execute(query)  # Send query to MySQL
    connection.commit()  # Save changes permanently
    cursor.close()  # Cleanup


def insert_mysql(server_information: dict, connection):

    if connection is None:
        return

    reset_mysql(connection)

    cursor = connection.cursor()  # Create cursor object

    for server in server_information.values():
        # SQL Query
        query = """
        INSERT INTO servers (identifier, server_name, player_count, max_players, current_state, uptime, ip, port, game_type, version, map, query_port, rcon, error)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        
        ON DUPLICATE KEY UPDATE
        player_count = %s,
        max_players = %s,
        current_state = %s,
        uptime = %s,
        version = %s,
        error = %s
        """

        try:
            values = (server.identifier, server.server_name, server.player_count, server.max_players, server.current_state,
                      server.uptime, server.ip, server.port, server.game_type, server.version, server.map,
                      server.query_port, server.rcon, server.error, server.player_count, server.max_players, server.current_state,
                      server.uptime, server.version, server.error)
        except AttributeError as e:
            logger('insert_mysql', f'Expected ServerType, got {type(server)}')
            continue

        cursor.execute(query, values)

    connection.commit()

    # Cleanup
    cursor.close()
    connection.close()
