import json
import bot_functions as bot
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os

load_dotenv()

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
        self.total_count = self.guild.member_count
        self.online_members = bot.get_online_members(self.guild.members, discord)

        if not self.update_data.is_running():
            self.update_data.start()


    # async def on_guild_channel_create(self, message):
    #     pass


# ********* LOOPS *************

    @tasks.loop(seconds=10.0)
    async def update_data(self):
        print("\n" * 2)

        self.player_activity = bot.get_member_activity(self.guild.members)

        if not self.player_activity:
            print(f'Online Members Count: {len(self.online_members)}/{self.total_count}')
            print(f"Members: {self.online_members}")
            print("No one is online...")
        else:
            self.game_count = bot.get_game_count(self.player_activity)
            bot.insert_mysql(self.game_count, bot.connect_mysql())
            
            
            # Pretty print ONLY for debugging/output
            print('********* DISCORD INFO **********')
            print(f'Online Members Count: {len(self.online_members)}/{self.total_count}')
            print(f"Members: {self.online_members}")
            print(json.dumps(self.player_activity, indent=4))
            print(json.dumps(self.game_count, indent=4))


intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

client = PlayerRebornBot(intents=intents)
client.run(TOKEN)