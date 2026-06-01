import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
from services.activity_service import get_member_info
from services.pterodactyl import get_all_server_data
import query_handlers.games_table_query as game_sql
import query_handlers.servers_table_query as server_sql
from services.mysql_login import login
# from utils.logger import logger

load_dotenv()

URL = "https://panel.playerreborn.com/api/"
PUBLIC_IP = "play.playerreborn.com"
TOKEN = os.getenv("TOKEN")
SERVER_ID = 1330977532824129616

class PlayerRebornBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.guild = None
        self.total_count = None
        self.online_members = None
        self.player_activity = {}
        self.game_count = {}

    async def on_connect(self):
        print('Connecting...')

    async def on_ready(self):
        print(f'{self.user} has connected to the server.')
        self.guild = self.get_guild(SERVER_ID)
        print('')


        if not self.update_data.is_running():
            self.update_data.start()

    # async def on_guild_channel_create(self, message):
    #     pass

    # ********* LOOPS *************

    @tasks.loop(seconds=10.0)
    async def update_data(self):

        player_manager = get_member_info(self.guild.members)
        server_manager = get_all_server_data(URL, PUBLIC_IP)

        if not player_manager.online_members:
            print("No Players are Online.")
            print('')
        else:

            game_sql.insert_mysql(
                connection=login(),
                activity=player_manager.activity_count
            )

        if not server_manager.servers:
            print("No Servers Are Playable")
            print('')
        else:
            server_sql.insert_mysql(
                connection=login(),
                server_information=server_manager.servers
            )




intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

client = PlayerRebornBot(intents=intents)
client.run(TOKEN)
