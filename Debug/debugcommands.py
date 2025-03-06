# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord import default_permissions
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Utilities.constants import DebugTexts, DebugLists, LoadOrder

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.debugmethods import DebugMethods

class DebugCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="announce", description=DebugTexts.C_ANNOUNCE, guild_ids=DebugLists.GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_announce(
            self,
            ctx: ApplicationContext,
            title: Option(str, DebugTexts.F_TITLE, required=True),
            description: Option(str, DebugTexts.F_DESCRIPTION, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)

        description = description.replace("\\n", "\n")
        embed: Embed = Embed(title=title, description=description, colour=0xFFFFFF)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.channel.send(embed=embed)
        await ctx.interaction.followup.send(content="Announcement created.")

    @commands.slash_command(name="shutdown", description=DebugTexts.C_SHUTDOWN, guild_ids=DebugLists.GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_shutdown(
            self,
            ctx: ApplicationContext):
        await ctx.interaction.response.defer(ephemeral=True)
        await ctx.interaction.followup.send(content="Shutting down.")

        exit(1)

    @commands.slash_command(name="reload", description=DebugTexts.C_RELOAD, guild_ids=DebugLists.GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_reload(
            self,
            ctx: ApplicationContext,
            cog: Option(str, DebugTexts.F_COG, choices=LoadOrder.COGS, required=True)):
        await ctx.interaction.response.defer(ephemeral=True)
        
        methods: DebugMethods
        if (methods := self.bot.get_cog("DebugMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.reload_cog(cog))
    
    @commands.slash_command(name="status", description=DebugTexts.C_STATUS, guild_ids=DebugLists.GUILDS)
    @default_permissions(administrator=True,)
    @try_func_async()
    async def slash_status(
            self,
            ctx: ApplicationContext):
        await ctx.interaction.response.defer(ephemeral=True)
        
        methods: DebugMethods
        if (methods := self.bot.get_cog("DebugMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.cog_status())


def setup(bot):
    bot.add_cog(DebugCommands(bot))