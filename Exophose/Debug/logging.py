from datetime import datetime, timedelta
import discord
from discord.bot import Bot
from discord.ext import commands
from discord.channel import TextChannel
from discord.embeds import Embed

class Logging(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def log_event (self, event: str, type: str) :
        """Prints an event in console. Console is saved as log."""

        localizeddatetime = datetime.now() - timedelta(hours=4)

        print(f' {type}  [{localizeddatetime.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {event}')

        consoleChannel: TextChannel = self.bot.get_channel("YOUR CHANNEL")

        await consoleChannel.send(f'```css\r\n[{type[:4]}] | [{localizeddatetime.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] | {event}\r\n```')

    async def log_error (self, error, function, traceback, *args) :
        """Logs an error."""

        localizeddatetime = datetime.now() - timedelta(hours=4)

        print(f' ERROR  [{localizeddatetime.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - Exophose encountered {error} in {function}.')

        epoch: int = int(datetime.now().timestamp())

        embed: Embed = discord.Embed(title=f"Error in Exophose", description=error, colour=0xCC0000)

        embed.add_field(name="Timestamp", value=f"<t:{epoch}:F>, <t:{epoch}:R>", inline=True)
        embed.add_field(name="Function", value=f"`{function}`", inline=True)
        embed.add_field(name="Traceback", value=f'`{traceback}`', inline=False)
        if len(args) > 0:
            embed.add_field(name="Arguments", value=f'`{args}`', inline=False)

        consoleChannel: TextChannel = self.bot.get_channel("YOUR CHANNEL")

        await consoleChannel.send(embed=embed, content="YOUR TAG")

    async def log_sql_error(self, error: str = "", function: str = "", guildid: str = None, userid: str = None, roleid: str = None):
        """Logs an error."""

        localizeddatetime = datetime.now() - timedelta(hours=4)

        print(f' ERROR  [{localizeddatetime.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - Exophose encountered {error} in {function}.')

        epoch: int = int(datetime.now().timestamp())

        embed: Embed = discord.Embed(title=f"SQL Error in Exophose", description=error, colour=0xCC0000)

        embed.add_field(name="Timestamp", value=f"<t:{epoch}:F>, <t:{epoch}:R>", inline=True)
        embed.add_field(name="Function", value=f"`{function}`", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        if guildid is not None:
            embed.add_field(name="Guild ID", value=f"`{guildid}`", inline=True)
        if userid is not None:
            embed.add_field(name="User ID", value=f"`{userid}`", inline=True)
        if roleid is not None:
            embed.add_field(name="Role ID", value=f"`{roleid}`", inline=True)

        consoleChannel: TextChannel = self.bot.get_channel("YOUR CHANNEL")

        await consoleChannel.send(embed=embed, content="YOUR TAG")


def setup(bot):
    bot.add_cog(Logging(bot))