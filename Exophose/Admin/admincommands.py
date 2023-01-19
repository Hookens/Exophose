import discord
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role
import traceback

class AdminCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="allow", description="Allow a role to use role management commands.", guild_only=True)
    @discord.default_permissions(administrator=True,)
    async def slash_allow(self, ctx: ApplicationContext, role: Option(Role, "The role you wish to allow.", required=True), maxroles: Option(int, "The maximum number of roles that a user with that role can create.", min_value=0, max_value=20, required=False) = 0, allowbadges: Option(bool, "If the users are allowed to add custom badges to their roles.", required=False, default=False) = False):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            methods = self.bot.get_cog("AdminMethods")

            if methods is not None:
                await ctx.interaction.followup.send(embed=await methods.allow_role(role, ctx, maxroles, allowbadges))

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e, 'admincommands - slash_allow', traceback.format_exc())

    @commands.slash_command(name="disallow", description="Disallow a role from using role management commands.", guild_only=True)
    @discord.default_permissions(administrator=True,)
    async def slash_disallow(self, ctx: ApplicationContext, role: Option(Role, "The role you wish to disallow.", required=True)):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            methods = self.bot.get_cog("AdminMethods")

            if methods is not None:
                await ctx.interaction.followup.send(embed=await methods.disallow_role(role, ctx))

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'admincommands - slash_disallow', traceback.format_exc())

    @commands.slash_command(name="allowed", description="List the currently allowed roles in your server.", guild_only=True)
    @discord.default_permissions(administrator=True,)
    async def slash_allowedroles(self, ctx: ApplicationContext, bypassephemeral: Option(bool, "If you wish to make this message public, to pin it for example.") = False):
        try:
            await ctx.interaction.response.defer(ephemeral=not bypassephemeral)
            
            embeds = self.bot.get_cog("Embeds")

            if embeds is not None:
                await ctx.interaction.followup.send(embed=await embeds.generate_embed_allowed_roles(str(ctx.guild.id)))

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e, 'admincommands - slash_allowedroles', traceback.format_exc())

def setup(bot):
    bot.add_cog(AdminCommands(bot))