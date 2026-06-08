from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from query_handlers.mysql_login import login

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/games_table',
         summary="Get approved games",
         description="Returns the top 6 approved games ordered by player count.")
def games_table():

    connection = login()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail='Database connection failed'
        )

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT 
    id,
    activity_code,
    game_name,
    player_count,
    game_image,
    approved
    FROM games
    WHERE approved = TRUE
    ORDER BY player_count DESC
    LIMIT 6
    """


    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    games = []

    for row in result:
        games.append( {
            'id': row['id'],
            'activity_code': row['activity_code'],
            'game_name': row['game_name'],
            'player_count': row['player_count'],
            'game_image': row['game_image'],
            'approved': row['approved']
        })

    return games

@app.get('/servers_table',
         summary="Get approved servers",
         description="Get all approved servers from the database.")
def servers_table():

    connection = login()

    if connection is None:
        raise HTTPException(
            status_code=500,
            detail='Database connection failed'
        )

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
    id,
    identifier,
    server_name,
    player_count,
    max_players,
    current_state,
    uptime,
    ip,
    port,
    game_type,
    approved,
    version,
    map,
    query_port,
    rcon,
    error
    FROM servers
    WHERE approved = TRUE
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    servers = []

    for row in result:
        servers.append({
            'id': row['id'],
            'identifier': row['identifier'],
            'server_name': row['server_name'],
            'player_count': row['player_count'],
            'max_players': row['max_players'],
            'current_state': row['current_state'],
            'uptime': row['uptime'],
            'ip': row['ip'],
            'port': row['port'],
            'game_type': row['game_type'],
            'approved': row['approved'],
            'version': row['version'],
            'map': row['map'],
            'query_port': row['query_port'],
            'rcon': row['rcon'],
            'error': row['error']
        })

    return servers

@app.get('/health')
def health():
    return {'status': 'online'}