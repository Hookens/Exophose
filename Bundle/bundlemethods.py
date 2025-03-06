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

class BundleMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_data: bool = False, include_embeds: bool = False, include_verification: bool = False) -> tuple:
        data = self.bot.get_cog("Data") if include_data else None
        embeds = self.bot.get_cog("Embeds") if include_embeds else None
        verification = self.bot.get_cog("Verification") if include_verification else None
        
        if ((data is None and include_data) or 
            (embeds is None and include_embeds) or
            (verification is None and include_verification)):
            raise(ValueError("One or more cogs are missing.", data, embeds, verification))
        
        return tuple(filter(None, (data, embeds, verification)))

    @try_func_async(embed=True)
    async def bundle_create(
            self,
            ctx: ApplicationContext,
            name: str) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)
        
        if not verification.is_name_allowed(name):
            return embeds.blacklisted_word()
        
        if await data.count_bundles(ctx.guild.id) >= 5:
            return embeds.maximum_bundles()

        if await data.add_bundle(ctx.guild.id, name):
            return embeds.bundle_created(name)

            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_list(
            self,
            ctx: ApplicationContext) -> Embed:
        embeds: 'Embeds'
        (embeds,) = self._get_cogs(include_embeds=True)

        return await embeds.bundle_list(ctx.guild.id)

    @try_func_async(embed=True)
    async def bundle_edit(
            self,
            ctx: ApplicationContext,
            index: int,
            role: Role,
            add: bool) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)
        
        if not (0 <= index < await data.count_bundles(ctx.guild.id)):
            return embeds.bundle_missing_index("edit")

        addable = await verification.is_bundle_role_addable(role.id, ctx.guild.id, index)

        if add:
            if not verification.is_name_allowed(role.name):
                return embeds.blacklisted_word()
                    
            if addable == 1:
                if await data.add_bundle_role(role.id, ctx.guild.id, index):
                    return embeds.bundle_role_added(role)
            elif addable == 0:
                return embeds.bundle_role_present(role)
            else:
                return embeds.bundle_role_error(role)

        else:
            if addable == 1:
                return embeds.bundle_role_missing(role)
            else:
                if await data.delete_bundle_role(role.id, ctx.guild.id, index):
                    return embeds.bundle_role_removed(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_delete(
            self,
            ctx: ApplicationContext,
            index: int,
            name: str) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)
        
        if not (0 <= index < await data.count_bundles(ctx.guild.id)):
            return embeds.bundle_missing_index("delete")
        
        if not await verification.is_bundle_selection_valid(ctx.guild.id, index, name):
            return embeds.bundle_selection_invalid()
        
        if await data.delete_bundle(ctx.guild.id, index):
            return embeds.bundle_deleted()
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_allow(
            self,
            ctx: ApplicationContext,
            index: int,
            role: Role) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)
        
        if not (0 <= index < await data.count_bundles(ctx.guild.id)):
            return embeds.bundle_missing_index("allow")
        
        if not verification.is_name_allowed(role.name):
                return embeds.blacklisted_word()
        
        allowable = await verification.is_bundle_allowed_role_allowable(role.id, ctx.guild.id, index)
        if allowable == 1:
            if await data.add_bundle_allowed_role(role.id, ctx.guild.id, index):
                return embeds.bundle_allowed_role_added(role)
        elif allowable == 0:
            return embeds.bundle_allowed_role_present(role)
        else:
            return embeds.bundle_allowed_role_error(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_disallow(
            self,
            ctx: ApplicationContext,
            index: int,
            role: Role) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)
        
        if not (0 <= index < await data.count_bundles(ctx.guild.id)):
            return embeds.bundle_missing_index("disallow")

        allowable = await verification.is_bundle_allowed_role_allowable(role.id, ctx.guild.id, index)
        if allowable == 1:
            return embeds.bundle_allowed_role_missing(role)
        else:
            if await data.delete_bundle_allowed_role(role.id, ctx.guild.id, index):
                return embeds.bundle_allowed_role_removed(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_choices(
            self,
            ctx: ApplicationContext) -> Embed:
        embeds: 'Embeds'
        verification: 'Verification'
        (embeds, verification) = self._get_cogs(include_embeds=True, include_verification=True)
        
        allowed_roles = await verification.get_allowed_bundle_roles(ctx.author)

        if not allowed_roles:
            return embeds.not_bundle_allowed()
        
        return await embeds.bundle_choices(allowed_roles)

    @try_func_async(embed=True)
    async def bundle_choose(
            self,
            ctx: ApplicationContext,
            index: int) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(True, True, True)

        allowed_roles = await verification.get_allowed_bundle_roles(ctx.author)

        if not allowed_roles:
            return embeds.not_bundle_allowed()
        
        if ((not await verification.check_user_bundle_roles(allowed_roles, ctx.author, True)) 
            or (not (0 <= index < await data.count_bundles_choices(allowed_roles)))):
            return embeds.bundle_missing_choice_index()
        
        chosen_role_id = await data.get_bundles_choice(allowed_roles, index)
        role: Role = ctx.guild.get_role(chosen_role_id)
        
        try:
            await ctx.author.add_roles(role)
        except:
            return embeds.not_role_allowed(role)

        return embeds.bundle_role_selected(role)
    
def setup(bot):
    bot.add_cog(BundleMethods(bot))