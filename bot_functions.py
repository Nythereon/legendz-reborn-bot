from typing import Sequence
import mysql.connector
import requests


def get_member_activity(members: Sequence):
    # Create a fresh dictionary every function call
    online_players = {}
    for member in members:
        # Skip members with no activity
        if member.activity is None:
            continue
        # Store:
        # username -> activity name
        online_players[member.display_name] = member.activity.name
    # Return the raw dictionary
    return online_players

def get_online_members(guild: Sequence, discord_client):
    return [member.display_name for member in guild
            if member.status == discord_client.Status.online and not member.bot]

def get_game_count(dictionary: dict):
    activity_dict = {}
    for activity in dictionary.values():
        if activity not in activity_dict:
            activity_dict[activity] = 1
        else:
            activity_dict[activity] += 1

    return activity_dict

def connect_mysql():
    # Connect to MySQL Server
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Play@time135',
        database='player_reborn'
    )
    return connection

def reset_mysql(connection):

    cursor = connection.cursor() # Create cursor object

    # SQL Query
    query = """
    UPDATE games
    SET players = 0
    """

    cursor.execute(query) # Send query to MySQL
    connection.commit() # Save changes permanently
    cursor.close() # Cleanup

def get_image(game_name):
    url = 'https://api.rawg.io/api/games'
    API_KEY = '430bf52ec9884f888b04d66b0c446935'

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

def insert_mysql(dictionary: dict, connection):

    reset_mysql(connection)
    inventory = dictionary # Data
    cursor = connection.cursor() # Create cursor object



    for game_name, player_count in inventory.items(): # Loop through dictionary

        # Check if game exists
        check_query = """
            SELECT activity_code
            FROM games
            WHERE activity_code = %s
            """

        cursor.execute(check_query, (game_name,))
        result = cursor.fetchone()

        if result:
            game_image = None
            print('Game Exists')
        else:
            game_image = get_image(game_name)

        # SQL Query
        query = """
        INSERT INTO games (activity_code, game_name, players, game_image)
        VALUES (%s, %s, %s, %s)
        
        ON DUPLICATE KEY UPDATE
        players = %s
        """

        values = (game_name, game_name, player_count, game_image, player_count) # Values for placeholders
        cursor.execute(query, values) # Send query to MySQL

    connection.commit() # Save changes permanently

    # Cleanup
    cursor.close()
    connection.close()

    print('Updated Database')

#TODO: Finish test_server.py and put here
def get_servers():
    pass
    # REAL PRINT from server_test.py goes here





# async def delete_chat(channel_id: int, client):
#     channel = client.get_channel(channel_id)
#     await channel.purge()
