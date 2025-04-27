# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import Attachment
from discord.bot import Bot
from discord.colour import Colour
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.constants import UserTexts
from Utilities.datahelpers import CreatedRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.utilities import Utilities
    from Utilities.verification import Verification

class UserMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_data: bool = False, include_embeds: bool = False, include_utilities: bool = False, include_verification: bool = False) -> tuple:
        data = self.bot.get_cog("Data") if include_data else None
        embeds = self.bot.get_cog("Embeds") if include_embeds else None
        utilities = self.bot.get_cog("Utilities") if include_utilities else None
        verification = self.bot.get_cog("Verification") if include_verification else None
        
        if ((data is None and include_data) or 
            (embeds is None and include_embeds) or 
            (utilities is None and include_utilities) or 
            (verification is None and include_verification)):
            raise(ValueError("One or more cogs are missing.", data, embeds, utilities, verification))
        
        return tuple(filter(None, (data, embeds, utilities, verification)))

    @try_func_async(embed=True)
    async def role_create (
            self,
            ctx: ApplicationContext,
            role_name: str,
            role_color: str,
            role_badge: Attachment) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        utilities: 'Utilities'
        verification: 'Verification'
        (data, embeds, utilities, verification) = self._get_cogs(True, True, True, True)

        if not verification.has_permission(ctx.guild):
            return embeds.not_permission_allowed()
        
        if not await verification.is_user_role_addable(ctx.guild.id, ctx.author):
            return embeds.maximum_roles()

        if not verification.is_name_allowed(role_name):
            return embeds.blacklisted_word()

        hex_color = await utilities.parse_color(role_color)

        if hex_color is None:
            return embeds.color_parsing_error(role_color)
        
        created_role: Role = await ctx.guild.create_role(name=role_name,colour=Colour(hex_color))
        if not await data.add_member_role(created_role.id, ctx.guild.id, ctx.author.id):
            await created_role.delete(reason=UserTexts.DELETE_REASON)
            return embeds.unexpected_sql_error()
        
        await ctx.author.add_roles(created_role)
        await utilities.reposition(created_role)
        embed: Embed = embeds.creation_success()

        if role_badge is not None:
            if "ROLE_ICONS" not in ctx.guild.features:
                embed.set_footer(text=UserTexts.DF_NO_PERMS)

            if not await verification.is_badge_allowed(ctx.guild.id, ctx.author):
                embed.set_footer(text=UserTexts.DF_NOT_ALLOWED)

            if not role_badge.content_type.startswith("image"):
                embed.set_footer(text=UserTexts.DF_INVALID_FILE)
            else:
                try:
                    await created_role.edit(icon=await role_badge.read())
                except:
                    pass

        return embed

    @try_func_async(embed=True)
    async def role_remove (
            self,
            ctx: ApplicationContext,
            role_index: int) -> Embed:
        embeds: 'Embeds'
        utilities: 'Utilities'
        verification: 'Verification'
        (embeds, utilities, verification) = self._get_cogs(include_embeds=True, include_utilities=True, include_verification=True)

        if not verification.has_permission(ctx.guild):
            return embeds.not_permission_allowed()
        
        if await utilities.delete_role(ctx.author, role_index):
            return embeds.success_modification("remove")
        
        return embeds.missing_modification_index("remove")

    @try_func_async(embed=True)
    async def role_recolor (
            self, 
            ctx: ApplicationContext, 
            role_color: str, 
            role_index: int) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        utilities: 'Utilities'
        verification: 'Verification'
        (data, embeds, utilities, verification) = self._get_cogs(True, True, True, True)

        if not verification.has_permission(ctx.guild):
            return embeds.not_permission_allowed()
        
        hex_color = await utilities.parse_color(role_color)

        if hex_color is None:
            return embeds.color_parsing_error()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(ctx.guild.id, ctx.author.id)

        if not any(created_roles):
            return embeds.missing_modification_role("recolor")
        
        if role_index >= len(created_roles):
            return embeds.missing_modification_index("recolor")
        
        role: Role = ctx.guild.get_role(created_roles[role_index].id)

        try:
            await role.edit(colour=Colour(hex_color))
        except:
            return embeds.not_edit_allowed(role, "recolor")

        return embeds.success_modification("recolor")
    
    @try_func_async(embed=True)
    async def role_rename (
            self, 
            ctx: ApplicationContext, 
            role_name: str, 
            role_index: int) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(include_data=True, include_embeds=True, include_verification=True)
        
        if not verification.has_permission(ctx.guild):
            return embeds.not_permission_allowed()

        if not verification.is_name_allowed(role_name):
            return embeds.blacklisted_word()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(ctx.guild.id, ctx.author.id)

        if not any(created_roles):
            return embeds.missing_modification_role("rename")
        
        if role_index >= len(created_roles):
            return embeds.missing_modification_index("rename")
        
        role: Role = ctx.guild.get_role(created_roles[role_index].id)

        try:
            await role.edit(name=role_name)
        except:
            return embeds.not_edit_allowed(role, "rename")
        
        return embeds.success_modification("rename")
    
    @try_func_async(embed=True)
    async def role_rebadge (
            self,
            ctx: ApplicationContext,
            role_badge: Attachment,
            role_index: int) -> Embed:
        data: 'Data'
        embeds: 'Embeds'
        verification: 'Verification'
        (data, embeds, verification) = self._get_cogs(include_data=True, include_embeds=True, include_verification=True)
        if "ROLE_ICONS" not in ctx.guild.features:
            return embeds.not_feature_allowed()
        
        if not verification.has_permission(ctx.guild):
            return embeds.not_permission_allowed()

        if not await verification.is_badge_allowed(ctx.guild.id, ctx.author):
            return embeds.not_badge_allowed()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(ctx.guild.id, ctx.author.id)

        if not any(created_roles):
            return embeds.missing_modification_role("rebadge")
        
        if role_index >= len(created_roles):
            return embeds.missing_modification_index("rebadge")
        
        role: Role = ctx.guild.get_role(created_roles[role_index].id)
        
        if role_badge is None:
            try:
                await role.edit(icon=None)
            except:
                return embeds.not_edit_allowed(role, "rebadge")
            
        elif role_badge.content_type.startswith("image"):
            try:
                await role.edit(icon=await role_badge.read())
                return embeds.success_modification("rebadge")
            except:
                pass

        return embeds.not_file_allowed()
    
def setup(bot):
    bot.add_cog(UserMethods(bot))