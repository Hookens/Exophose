# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Help.helpview import HelpView
from Utilities.constants import HelpTexts

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Help.helpmethods import HelpMethods

class HelpCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="help", description=HelpTexts.C_HELP, guild_only=True)
    @try_func_async()
    async def slash_help(
            self,
            ctx: ApplicationContext,
            public: Option(bool, HelpTexts.F_PUBLIC) = False):
        await ctx.interaction.response.defer(ephemeral=not public)

        methods: HelpMethods
        if (methods := self.bot.get_cog("HelpMethods")) is not None:
            await ctx.interaction.followup.send(embed=await methods.generate_help(), view=HelpView(self.bot))

def setup(bot):
    bot.add_cog(HelpCommands(bot))