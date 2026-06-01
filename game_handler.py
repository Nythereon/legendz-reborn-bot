from query_handlers.minecraft_query import get_minecraft
from query_handlers.steam_query import get_steam_servers

GAME_HANDLERS = {
    'Paper': get_minecraft,
    'Forge': get_minecraft,
    'Fabric': get_minecraft,
    'Conan Exiles Enhanced Linux': get_steam_servers
}