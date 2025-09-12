# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

import discord
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.constants import AdminTexts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Admin.adminmethods import AdminMethods
    from Utilities.embeds import Embeds

class AdminCommands(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="allow", description=AdminTexts.C_ALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_allow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, AdminTexts.F_ALLOWROLE, required=True),
            max_roles: Option(int, AdminTexts.F_MAX, min_value=1, max_value=20, required=False),
            allow_gradients: Option(bool, AdminTexts.F_GRADIENTS, required=False),
            allow_badges: Option(bool, AdminTexts.F_BADGES, required=False)):
        await ctx.interaction.response.defer(ephemeral=True)
        
        methods: 'AdminMethods'
        if (methods := self.bot.get_cog("AdminMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.allow_role(ctx, role, max_roles, allow_gradients, allow_badges))

    @commands.slash_command(name="disallow", description=AdminTexts.C_DISALLOW, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_disallow(
            self,
            ctx: ApplicationContext,
            role: Option(Role, AdminTexts.F_DISALLOWROLE, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)
        
        methods: 'AdminMethods'
        if (methods := self.bot.get_cog("AdminMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.disallow_role(ctx, role))

    @commands.slash_command(name="allowed", description=AdminTexts.C_ALLOWED, guild_only=True)
    @discord.default_permissions(administrator=True,)
    @try_func_async()
    async def slash_allowedroles(
            self,
            ctx: ApplicationContext,
            public: Option(bool, AdminTexts.F_PUBLIC) = False):
        await ctx.interaction.response.defer(ephemeral=not public)
        
        embeds: 'Embeds'
        if (embeds := self.bot.get_cog("Embeds")) is not None:
            await ctx.interaction.followup.send(embed=await embeds.allowed_roles(ctx.guild.id))

def setup(bot):
    bot.add_cog(AdminCommands(bot))