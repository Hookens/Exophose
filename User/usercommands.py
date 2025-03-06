# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import SlashCommandOptionType
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.member import Member

from Debug.debughelpers import try_func_async
from Utilities.constants import UserTexts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from User.usermethods import UserMethods
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification

class UserCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_embeds: bool = False, include_methods: bool = False, include_verification: bool = False) -> tuple:
        embeds = self.bot.get_cog("Embeds") if include_embeds else None
        methods = self.bot.get_cog("UserMethods") if include_methods else None
        verification = self.bot.get_cog("Verification") if include_verification else None
        
        if ((embeds is None and include_embeds) or 
            (methods is None and include_methods) or 
            (verification is None and include_verification)):
            raise(ValueError("One or more cogs are missing.", embeds, methods, verification))
        
        return tuple(filter(None, (embeds, methods, verification)))
    
    async def allowed(self, ctx: ApplicationContext) -> bool:
        embeds: 'Embeds'
        verification: 'Verification'
        (embeds, verification) = self._get_cogs(include_embeds=True, include_verification=True)

        await ctx.interaction.response.defer(ephemeral=True)

        if not (allowed := await verification.is_user_allowed(ctx.author)):
            await ctx.interaction.followup.send(embed=embeds.not_user_allowed())

        return allowed

    @commands.slash_command(name="create", description=UserTexts.C_CREATE, guild_only=True)
    @try_func_async()
    async def slash_create(
            self,
            ctx: ApplicationContext,
            name: Option(str, UserTexts.F_NAME, max_length=100, required=True),
            color: Option(str, UserTexts.F_COLOR, max_length=7, required=True),
            badge: Option(SlashCommandOptionType.attachment, UserTexts.F_BADGE, required=False) = None):
        methods: 'UserMethods'
        (methods,) = self._get_cogs(include_methods=True)

        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await methods.role_create(ctx, name, color, badge))

    @commands.slash_command(name="remove", description=UserTexts.C_REMOVE, guild_only=True)
    @try_func_async()
    async def slash_remove(
            self,
            ctx: ApplicationContext,
            index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
        methods: 'UserMethods'
        (methods,) = self._get_cogs(include_methods=True)

        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await methods.role_remove(ctx, index))

    @commands.slash_command(name="recolor", description=UserTexts.C_RECOLOR, guild_only=True)
    @try_func_async()
    async def slash_recolor(
            self,
            ctx: ApplicationContext,
            color: Option(str, UserTexts.F_COLOR, max_length=7, required=True),
            index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
        methods: 'UserMethods'
        (methods,) = self._get_cogs(include_methods=True)

        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await methods.role_recolor(ctx, color, index))

    @commands.slash_command(name="rename", description=UserTexts.C_RENAME, guild_only=True)
    @try_func_async()
    async def slash_rename(
            self,
            ctx: ApplicationContext,
            name: Option(str, UserTexts.F_NAME, max_length=100, required=True),
            index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
        methods: 'UserMethods'
        (methods,) = self._get_cogs(include_methods=True)

        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await methods.role_rename(ctx, name, index))

    @commands.slash_command(name="rebadge", description=UserTexts.C_REBADGE, guild_only=True)
    @try_func_async()
    async def slash_rebadge(
            self,
            ctx: ApplicationContext,
            badge: Option(SlashCommandOptionType.attachment, UserTexts.F_BADGE, required=False) = None,
            index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
        methods: 'UserMethods'
        (methods,) = self._get_cogs(include_methods=True)

        if await self.allowed(ctx):
                    await ctx.interaction.followup.send(embed=await methods.role_rebadge(ctx, badge, index))

    @commands.slash_command(name="created", description=UserTexts.C_CREATED, guild_only=True)
    @try_func_async()
    async def slash_created(
            self,
            ctx: ApplicationContext,
            member: Option(Member, UserTexts.F_MEMBER, required=False) = None):
        embeds: 'Embeds'
        (embeds,) = self._get_cogs(include_embeds=True)
        
        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await embeds.created_roles(member or ctx.author))

    @commands.slash_command(name="preview", description=UserTexts.C_PREVIEW, guild_only=True)
    @try_func_async()
    async def slash_preview(
            self,
            ctx: ApplicationContext,
            color: Option(str, UserTexts.F_PREVIEW, required=False) = None):
        embeds: 'Embeds'
        (embeds,) = self._get_cogs(include_embeds=True)
        
        if await self.allowed(ctx):
            await ctx.interaction.followup.send(embed=await embeds.preview_color(ctx.author, color))

def setup(bot):
    bot.add_cog(UserCommands(bot))