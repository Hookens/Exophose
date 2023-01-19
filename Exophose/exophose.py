#====== Exophose by Hookens#2000 =======
import discord
from discord.ext import commands

intents = discord.Intents().default()
intents.members = True
exophoseClient = commands.Bot(intents=intents, help_command=None)

exophoseClient.load_extension("Debug.logging")
exophoseClient.load_extension("Utilities.events")
exophoseClient.load_extension("Utilities.data")
exophoseClient.load_extension("Utilities.embeds")
exophoseClient.load_extension("Debug.debugmethods")
exophoseClient.load_extension("Debug.debugcommands")
exophoseClient.load_extension("Utilities.utilities")
exophoseClient.load_extension("Utilities.verification")
exophoseClient.load_extension("Admin.adminmethods")
exophoseClient.load_extension("Admin.admincommands")
exophoseClient.load_extension("User.usermethods")
exophoseClient.load_extension("User.usercommands")

exophoseClient.run("YOUR TOKEN")

