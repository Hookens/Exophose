from datetime import datetime
import discord
from discord.bot import Bot
from discord.ext import commands
from discord.channel import TextChannel
from discord.embeds import Embed

NAME = "Exophose"
CHANNEL = 890207343294447647 #PROD CHANNEL = 890207343294447647   |   DEV CHANNEL = 908734633569574932
PING = 320214798640087040

class Logging(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def log_event (self, event: str, type: str):
        print(f' {type}  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {event}')

        console_channel: TextChannel = self.bot.get_channel(CHANNEL)

        await console_channel.send(content=f"```prolog\r\n{event}```")

    async def log_error (self, error, function, traceback, *args):
        print(f' ERROR  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {NAME} encountered {error} in {function}.')

        epoch: int = int(datetime.now().timestamp())

        embed: Embed = discord.Embed(title=f"Error in {NAME}", description=error, colour=0xCC0000)

        embed.add_field(name="Timestamp", value=f"<t:{epoch}:F>, <t:{epoch}:R>", inline=True)
        embed.add_field(name="Function", value=f"`{function}`", inline=True)
        embed.add_field(name="Traceback", value=f'`{traceback}`', inline=False)
        if any(args):
            embed.add_field(name="Arguments", value=f'`{args}`', inline=False)

        console_channel: TextChannel = self.bot.get_channel(CHANNEL)

        await console_channel.send(embed=embed, content=f"<@{PING}>")


def setup(bot):
    bot.add_cog(Logging(bot))