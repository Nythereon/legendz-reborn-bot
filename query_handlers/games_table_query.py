from services.rawg_service import get_image

def reset_mysql(connection):
    cursor = connection.cursor()  # Create cursor object

    # SQL Query
    query = """
    UPDATE games
    SET player_count = 0
    """

    cursor.execute(query)  # Send query to MySQL
    connection.commit()  # Save changes permanently
    cursor.close()  # Cleanup

def insert_mysql(activity: dict, connection):
    reset_mysql(connection)

    cursor = connection.cursor()  # Create cursor object

    for activity_code, count in activity.items():  # Loop through dictionary
        player_count = count
        # Check if game exists
        check_query = """
            SELECT activity_code
            FROM games
            WHERE activity_code = %s
            """

        cursor.execute(check_query, (activity_code,))
        result = cursor.fetchone()

        if result:
            game_image = None
            print(f'Game image already exists for {activity_code}.')

        else:
            game_image = get_image(activity_code)
            print(f'Grabbing image for {activity_code}.')

        # SQL Query
        query = """
        INSERT INTO games (activity_code, game_name, player_count, game_image)
        VALUES (%s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
        player_count = %s
        """

        values = (activity_code, activity_code, player_count, game_image, player_count)  # Values for placeholders
        cursor.execute(query, values)  # Send query to MySQL

    connection.commit()  # Save changes permanently

    # Cleanup
    cursor.close()
    connection.close()
    print('Updated Games Table')

    return None
