from discord.bot import Bot
from discord.ext import commands
from discord.embeds import Embed

from Debug.debughelpers import try_func_async

class DebugMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cog(self) -> tuple:
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

        admincommands = self.bot.get_cog("AdminCommands") 
        adminmethods = self.bot.get_cog("AdminMethods") 
        debugcommands = self.bot.get_cog("DebugCommands") 
        debugmethods = self.bot.get_cog("DebugMethods") 
        usercommands = self.bot.get_cog("UserCommands") 
        usermethods = self.bot.get_cog("UserMethods") 
        data = self.bot.get_cog("Data") 
        embeds = self.bot.get_cog("Embeds") 
        events = self.bot.get_cog("Events") 
        help = self.bot.get_cog("Help") 
        logging = self.bot.get_cog("Logging") 
        utilities = self.bot.get_cog("Utilities") 
        verification = self.bot.get_cog("Verification") 

        embed.add_field(name="Admin", value=f"{'🟢' if admincommands is not None else '🔴' } AdminCommands\n{'🟢' if adminmethods is not None else '🔴' } AdminMethods", inline=False)
        embed.add_field(name="Debug", value=f"{'🟢' if debugcommands is not None else '🔴' } DebugCommands\n{'🟢' if debugmethods is not None else '🔴' } DebugMethods\n{'🟢' if logging is not None else '🔴' } Logging", inline=False)
        embed.add_field(name="User", value=f"{'🟢' if usercommands is not None else '🔴' } UserCommands\n{'🟢' if usermethods is not None else '🔴' } UserMethods", inline=False)
        embed.add_field(name="Utilities", value=f"{'🟢' if data is not None else '🔴' } Data\n{'🟢' if embeds is not None else '🔴' } Embeds\n{'🟢' if events is not None else '🔴' } Events\n{'🟢' if help is not None else '🔴' } Help\n{'🟢' if utilities is not None else '🔴' } Utilities\n{'🟢' if verification is not None else '🔴' } Verification", inline=False)
        embed.add_field(name="Server Count", value=f"Serving {len(self.bot.guilds)} servers")
        
        embed.description = f"{len(self.bot.cogs)} of 13 cogs working."

        return embed


def setup(bot):
    bot.add_cog(DebugMethods(bot))