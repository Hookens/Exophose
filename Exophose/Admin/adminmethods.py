from discord.bot import Bot
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async

class AdminMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self) -> tuple:
        data = self.bot.get_cog("Data")
        verification = self.bot.get_cog("Verification")
        embeds = self.bot.get_cog("Embeds")
        
        if data is None or verification is None or embeds is None:
            raise(ValueError("One or more cogs are missing.", data, verification, embeds))
        
        return (data, verification, embeds)

    @try_func_async(embed=True)
    async def allow_role(
            self,
            ctx: ApplicationContext,
            role: Role,
            max_roles: int,
            allow_badges: bool) -> Embed:
        (data, verification, embeds) = self._get_cogs()

        if not verification.is_role_name_allowed(role.name):
            return embeds.blacklisted_word()

        allowable = await verification.is_role_allowable(role.id, ctx.guild.id)
        if allowable == 0:
            return embeds.allowed_role_error(role)
        elif allowable == 1:
            if await data.add_allowed_role(role.id, ctx.guild.id, ctx.author.id, max_roles or 1, allow_badges):
                return embeds.allowed_role_added(role)
        elif allowable == 2:
            if await data.add_allowed_role(role.id, ctx.guild.id, ctx.author.id, max_roles, allow_badges):
                return embeds.allowed_role_updated(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def disallow_role(
            self,
            ctx: ApplicationContext,
            role: Role) -> Embed:
        (data, verification, embeds) = self._get_cogs()
        
        if await verification.is_role_allowable(role.id, ctx.guild.id) != 2:
            return embeds.allowed_role_missing(role)
        
        if await data.delete_allowed_role(role.id):
            return embeds.allowed_role_removed(role)

def setup(bot):
    bot.add_cog(AdminMethods(bot))