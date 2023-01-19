import discord
from datetime import datetime
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands
from discord.role import Role
import traceback

COGS = ["Admin.admincommands",
        "Admin.adminmethods", 
        "Debug.debugcommands", 
        "Debug.debugmethods", 
        "User.usercommands", 
        "User.usermethods", 
        "Utilities.data", 
        "Utilities.embeds", 
        "Utilities.events", 
        "Utilities.utilities", 
        "Utilities.verification"]

class DebugCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="announce", description="Make an announcement embed.", guild_ids=["YOUR GUILD ID",])
    @discord.default_permissions(administrator=True,)
    async def slash_announce(self, ctx: ApplicationContext, title: Option(str, "Title for the announcement.", required=True), description: Option(str, "Description for the announcement.", required=True)):
        try:
            await ctx.interaction.response.defer(ephemeral=True)

            description = description.replace("\\n", "\n")
            embed: Embed = Embed(title=title, description=description, colour=0xFFFFFF)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.channel.send(embed=embed)
            await ctx.interaction.followup.send(content="Announcement created.")

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e, 'debugcommands - slash_announce', traceback.format_exc())

    @commands.slash_command(name="reload", description="Reload a cog.", guild_ids=["YOUR GUILD ID",])
    @discord.default_permissions(administrator=True,)
    async def slash_reload(self, ctx: ApplicationContext, cog: Option(str, "Cog that needs to be reloaded.", choices=COGS, required=True)):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            methods = self.bot.get_cog("DebugMethods")

            if methods is not None:
                await ctx.interaction.followup.send(embed=await methods.reload_cog(cog))

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e, 'debugcommands - slash_reload', traceback.format_exc())
    
    @commands.slash_command(name="status", description="Get bot cogs' status.", guild_ids=["YOUR GUILD ID",])
    @discord.default_permissions(administrator=True,)
    async def slash_status(self, ctx: ApplicationContext):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            methods = self.bot.get_cog("DebugMethods")

            if methods is not None:
                await ctx.interaction.followup.send(embed=await methods.cog_status())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e, 'debugcommands - slash_status', traceback.format_exc())


def setup(bot):
    bot.add_cog(DebugCommands(bot))