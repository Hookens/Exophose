import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from Utilities.constants import Env, LoadOrder

load_dotenv()
TOKEN = os.getenv(Env.API_TOKEN)

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(intents=intents, help_command=None)

for COG in LoadOrder.COGS:
    client.load_extension(COG)

client.run(TOKEN)