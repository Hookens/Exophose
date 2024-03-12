from discord.bot import Bot
from discord.ext import commands
from discord.embeds import Embed

from Debug.debughelpers import try_func_async
from Utilities.constants import DebugLists, LoggingDefaults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.embeds import Embeds

class DebugMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cog(self) -> 'Embeds':
        embeds = self.bot.get_cog("Embeds")
        
        if embeds is None:
            raise(ValueError("Embeds cog missing.", embeds))
        
        return embeds

    @try_func_async(embed=True)
    async def reload_cog(self, cogname: str) -> Embed:
        embeds = self._get_cog()

        try:
            self.bot.unload_extension(cogname)
        except:
            pass

        try:
            self.bot.load_extension(cogname)
        except:
            return embeds.cog_restart_error(cogname)
        
        return embeds.cog_restarted(cogname)

    @try_func_async(embed=True)
    async def cog_status(self) -> Embed:
        embeds = self._get_cog()
        
        embed: Embed = embeds.generate_embed("Cog Statuses", "", 0xFFFFFF)

        cogdict = {}
        for cog in DebugLists.COGS:
            cogdict[cog] = self.bot.get_cog(cog)
            
        admincogs = {k:v for (k,v) in cogdict.items() if "Admin" in k}
        bundlecogs = {k:v for (k,v) in cogdict.items() if "Bundle" in k}
        debugcogs = {k:v for (k,v) in cogdict.items() if "Debug" in k}
        helpcogs = {k:v for (k,v) in cogdict.items() if "Help" in k}
        usercogs = {k:v for (k,v) in cogdict.items() if "User" in k}
        othercogs = {k:v for (k,v) in cogdict.items() if "Admin" not in k and "Bundle" not in k and "Debug" not in k and "Help" not in k and "User" not in k}

        adminfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in admincogs.items()])
        bundlefields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in bundlecogs.items()])
        debugfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in debugcogs.items()])
        helpfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in helpcogs.items()])
        userfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in usercogs.items()])
        otherfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in othercogs.items()])

        embed.add_field(name="Admin", value=adminfields, inline=False)
        embed.add_field(name="Bundle", value=bundlefields, inline=False)
        embed.add_field(name="Debug", value=debugfields, inline=False)
        embed.add_field(name="Help", value=helpfields, inline=False)
        embed.add_field(name="User", value=userfields, inline=False)
        embed.add_field(name="Utilities", value=otherfields, inline=False)
        embed.add_field(name="Server Count", value=f"Serving {len(self.bot.guilds)} servers")
        
        embed.description = f"{len(self.bot.cogs)} of {LoggingDefaults.COG_COUNT} cogs working."

        return embed


def setup(bot):
    bot.add_cog(DebugMethods(bot))