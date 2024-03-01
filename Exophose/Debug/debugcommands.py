from discord import default_permissions
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async

#Defines which guilds can access debug commands.
GUILDS = [
    858709508561436714,
]

COGS = [
    "Admin.admincommands",
    "Admin.adminmethods", 
    "Debug.debugcommands", 
    "Debug.debugmethods", 
    "User.usercommands", 
    "User.usermethods", 
    "Utilities.data", 
    "Utilities.embeds", 
    "Utilities.events", 
    "Utilities.help", 
    "Utilities.utilities", 
    "Utilities.verification",
]

C_ANNOUNCE = "Make an announcement embed."
C_SHUTDOWN = "Ends the bot thread."
C_RELOAD = "Reload a cog."
C_STATUS = "Get bot cogs' status."

F_TITLE = "Title for the announcement."
F_DESCRIPTION = "Description for the announcement."
F_COG = "Cog that needs to be reloaded."

class DebugCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="announce", description=C_ANNOUNCE, guild_ids=GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_announce(
            self,
            ctx: ApplicationContext,
            title: Option(str, F_TITLE, required=True),
            description: Option(str, F_DESCRIPTION, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)

        description = description.replace("\\n", "\n")
        embed: Embed = Embed(title=title, description=description, colour=0xFFFFFF)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)
        await ctx.interaction.followup.send(content="Announcement created.")

    @commands.slash_command(name="shutdown", description=C_SHUTDOWN, guild_ids=GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_shutdown(
            self,
            ctx: ApplicationContext):
        await ctx.interaction.response.defer(ephemeral=True)
        await ctx.interaction.followup.send(content="Shutting down.")

        exit(1)

    @commands.slash_command(name="reload", description=C_RELOAD, guild_ids=GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_reload(
            self,
            ctx: ApplicationContext,
            cog: Option(str, F_COG, choices=COGS, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)
        
        if (methods := self.bot.get_cog("DebugMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.reload_cog(cog))
    
    @commands.slash_command(name="status", description=C_STATUS, guild_ids=GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_status(
            self,
            ctx: ApplicationContext):
        await ctx.interaction.response.defer(ephemeral=True)
        
        if (methods := self.bot.get_cog("DebugMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.cog_status())


def setup(bot):
    bot.add_cog(DebugCommands(bot))