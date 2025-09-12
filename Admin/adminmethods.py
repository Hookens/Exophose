# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification

class AdminMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self) -> tuple['Data', 'Embeds', 'Verification']:
        data = self.bot.get_cog("Data")
        embeds = self.bot.get_cog("Embeds")
        verification = self.bot.get_cog("Verification")
        
        if data is None or embeds is None or verification is None:
            raise(ValueError("One or more cogs are missing.", data, embeds, verification))
        
        return (data, embeds, verification)

    @try_func_async(embed=True)
    async def allow_role(
            self,
            ctx: ApplicationContext,
            role: Role,
            max_roles: int,
            allow_gradients: bool,
            allow_badges: bool) -> Embed:
        (data, embeds, verification) = self._get_cogs()

        if not verification.is_name_allowed(role.name):
            return embeds.blacklisted_word()

        allowable, allowed_role = await verification.is_role_allowable(role.id, ctx.guild.id)
        if allowable == 0:
            return embeds.allowed_role_error(role)
        elif allowable == 1:
            if await data.add_allowed_role(role.id, ctx.guild.id, ctx.author.id, max_roles or 1, allow_badges or False, allow_gradients or False):
                return embeds.allowed_role_added(role)
        elif allowable == 2:
            print(allowed_role.max_roles, allowed_role.allow_badges, allowed_role.allow_gradients)
            if await data.add_allowed_role(role.id, ctx.guild.id, ctx.author.id,
                                           max_roles or allowed_role.max_roles,
                                           allow_badges or allowed_role.allow_badges,
                                           allow_gradients or allowed_role.allow_gradients):
                return embeds.allowed_role_updated(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def disallow_role(
            self,
            ctx: ApplicationContext,
            role: Role) -> Embed:
        (data, embeds, verification) = self._get_cogs()
        
        if await verification.is_role_allowable(role.id, ctx.guild.id) != 2:
            return embeds.allowed_role_missing(role)
        
        if await data.delete_allowed_role(role.id):
            return embeds.allowed_role_removed(role)

def setup(bot):
    bot.add_cog(AdminMethods(bot))