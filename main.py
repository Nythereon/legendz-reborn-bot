import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
from services.activity_service import get_member_info
from services.pterodactyl import get_all_server_data
import query_handlers.games_table_query as game_sql
import query_handlers.servers_table_query as server_sql
from query_handlers.mysql_login import login

load_dotenv()

URL = os.getenv('URL')
PUBLIC_IP = os.getenv('PUBLIC_IP')
TOKEN = os.getenv("TOKEN")
SERVER_ID = int(os.getenv('SERVER_ID'))
GENERAL_CHAT_ID = int(os.getenv('GENERAL_CHAT_ID'))

class PlayerRebornBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.guild = None

    async def on_ready(self):
        self.guild = self.get_guild(SERVER_ID)

        if not self.update_data.is_running():
            self.update_data.start()

    async def on_member_join(self, member):
        channel = self.get_channel(GENERAL_CHAT_ID)
        if channel:
            await channel.send(f"🎉 Welcome {member.mention}! Glad to have you here.")


    # ********* LOOPS *************

    @tasks.loop(seconds=5.0)
    async def update_data(self):

        if self.guild is None:
            return

        player_manager = get_member_info(self.guild.members)
        server_manager = get_all_server_data(URL, PUBLIC_IP)

        game_sql.insert_mysql(
            connection=login(),
            activity=player_manager.activity_count
        )

        if not server_manager.servers:
            print("No server data received.")
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
