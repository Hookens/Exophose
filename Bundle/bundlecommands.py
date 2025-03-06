# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

import discord
from discord import SlashCommandGroup
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.constants import BundleTexts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Bundle.bundlemethods import BundleMethods

class BundleCommands(commands.Cog):
    bundle = SlashCommandGroup("bundle", "Bundle related commands", guild_only=True)
    
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cog(self) -> 'BundleMethods':
        methods = self.bot.get_cog("BundleMethods")
        
        if methods is None:
            raise(ValueError("BundleMethods cog missing.", methods))
        
        return methods

    @bundle.command(name="create", description=BundleTexts.C_CREATE, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_create(
            self,
            ctx: ApplicationContext,
            name: Option(str, BundleTexts.F_NAME, max_length=100, required=True)):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_create(ctx, name))

    @bundle.command(name="list", description=BundleTexts.C_LIST, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_list(
            self,
            ctx: ApplicationContext):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_list(ctx))

    @bundle.command(name="edit", description=BundleTexts.C_EDIT, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_edit(
            self,
            ctx: ApplicationContext,
            role: Option(Role, BundleTexts.F_ROLE, required=True),
            index: Option(int, BundleTexts.F_INDEX, min_value=0, max_value=4, required=True),
            action: Option(str, BundleTexts.F_ACTION, choices=BundleTexts.CHOICES, default=BundleTexts.CHOICES[0])):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_edit(ctx, index, role, action == BundleTexts.CHOICES[0]))

    @bundle.command(name="delete", description=BundleTexts.C_DELETE, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_delete(
            self,
            ctx: ApplicationContext,
            name: Option(str, BundleTexts.F_CONFIRM, max_length=100, required=True),
            index: Option(int, BundleTexts.F_INDEX, min_value=0, max_value=4, required=True)):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_delete(ctx, index, name))

    @bundle.command(name="allow", description=BundleTexts.C_ALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_allow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, BundleTexts.F_ALLOWROLE, required=True),
            index: Option(int, BundleTexts.F_INDEX, min_value=0, max_value=4, required=True)):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_allow(ctx, index, role))

    @bundle.command(name="disallow", description=BundleTexts.C_DISALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_disallow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, BundleTexts.F_DISALLOWROLE, required=True),
            index: Option(int, BundleTexts.F_INDEX, min_value=0, max_value=4, required=True)):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_disallow(ctx, index, role))

    @bundle.command(name="choices", description=BundleTexts.C_CHOICES, guild_only=True)
    @try_func_async()
    async def slash_choices(
            self,
            ctx: ApplicationContext):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_choices(ctx))

    @bundle.command(name="choose", description=BundleTexts.C_CHOOSE, guild_only=True)
    @try_func_async()
    async def slash_choices(
            self,
            ctx: ApplicationContext,
            index: Option(int, BundleTexts.F_INDEX, min_value=0, max_value=9, required=True)):
        methods = self._get_cog()

        await ctx.interaction.response.defer(ephemeral=True)
        
        await ctx.interaction.followup.send(embed=await methods.bundle_choose(ctx, index))

def setup(bot):
    bot.add_cog(BundleCommands(bot))