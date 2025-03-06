# Copyright (C) 2025 Hookens
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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