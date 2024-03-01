import discord
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async

C_ALLOW = "Allow a role to use role management commands."
C_DISALLOW = "Disallow a role from using role management commands."
C_ALLOWED = "List the currently allowed roles in your server."

F_ALLOW = "The role you wish to allow."
F_DISALLOW = "The role you wish to disallow."
F_MAX = "The maximum number of roles that a user with that role can create."
F_BADGES = "If the users are allowed to add custom badges to their roles."
F_PUBLIC = "If you wish to make this message public."

class AdminCommands(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="allow", description=C_ALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_allow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, F_ALLOW, required=True),
            max_roles: Option(int, F_MAX, min_value=1, max_value=20, required=False) = 0,
            allow_badges: Option(bool, F_BADGES, required=False) = False):
        await ctx.interaction.response.defer(ephemeral=True)
        
        if (methods := self.bot.get_cog("AdminMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.allow_role(ctx, role, max_roles, allow_badges))

    @commands.slash_command(name="disallow", description=C_DISALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_disallow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, F_DISALLOW, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)
        
        if (methods := self.bot.get_cog("AdminMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.disallow_role(ctx, role))

    @commands.slash_command(name="allowed", description=C_ALLOWED, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_allowedroles(
            self,
            ctx: ApplicationContext,
            public: Option(bool, F_PUBLIC) = False):
        await ctx.interaction.response.defer(ephemeral=not public)
        
        if (embeds := self.bot.get_cog("Embeds")) is not None:
            await ctx.interaction.followup.send(embed=await embeds.allowed_roles(ctx.guild.id))

def setup(bot):
    bot.add_cog(AdminCommands(bot))