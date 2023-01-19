import discord
from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.embeds import Embed
from discord.role import Role
import traceback

class DebugMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def reload_cog(self, cogname: str) -> Embed:
        try:
            embeds = self.bot.get_cog("Embeds")
            
            if embeds is not None:
                if cogname is not None:
                    try:
                        self.bot.unload_extension(cogname)
                    except:
                        pass

                    try:
                        self.bot.load_extension(cogname)
                    except:
                        return await embeds.generate_cog_restart_error(cogname)
                    return await embeds.generate_cog_restarted(cogname)
                return await embeds.generate_no_cog_found(cogname)
            
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'debugmethods - reload_cog', traceback.format_exc())
            
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def cog_status(self) -> Embed:
        try:
            embeds = self.bot.get_cog("Embeds")
            
            if embeds is not None:
                cogcheck:int = 0
                embed: Embed = await embeds.generate_embed("Cog Statuses", "Verifying...", 0xFFFFFF)

                admincommands = self.bot.get_cog("AdminCommands") 
                adminmethods = self.bot.get_cog("AdminMethods") 
                debugcommands = self.bot.get_cog("DebugCommands") 
                debugmethods = self.bot.get_cog("DebugMethods") 
                usercommands = self.bot.get_cog("UserCommands") 
                usermethods = self.bot.get_cog("UserMethods") 
                data = self.bot.get_cog("Data") 
                embeds = self.bot.get_cog("Embeds") 
                events = self.bot.get_cog("Events")
                logging = self.bot.get_cog("Logging") 
                utilities = self.bot.get_cog("Utilities") 
                verification = self.bot.get_cog("Verification") 

                embed.add_field(name="Admin", value=f"AdminCommands {'🟢' if admincommands is not None else '🔴' }\nAdminMethods {'🟢' if adminmethods is not None else '🔴' }", inline=False)
                embed.add_field(name="Debug", value=f"DebugCommands {'🟢' if debugcommands is not None else '🔴' }\nDebugMethods {'🟢' if debugmethods is not None else '🔴' }\nLogging {'🟢' if logging is not None else '🔴' }", inline=False)
                embed.add_field(name="User", value=f"UserCommands {'🟢' if usercommands is not None else '🔴' }\nUserMethods {'🟢' if usermethods is not None else '🔴' }", inline=False)
                embed.add_field(name="Utilities", value=f"Data {'🟢' if data is not None else '🔴' }\nEmbeds {'🟢' if embeds is not None else '🔴' }\nEvents {'🟢' if events is not None else '🔴' }\nUtilities {'🟢' if utilities is not None else '🔴' }\nVerification {'🟢' if verification is not None else '🔴' }", inline=False)
                embed.add_field(name="Server Count", value=f"Serving {len(self.bot.guilds)} servers")
                
                if admincommands is not None: 
                    cogcheck += 1
                if adminmethods is not None: 
                    cogcheck += 1
                if debugcommands is not None: 
                    cogcheck += 1
                if debugmethods is not None: 
                    cogcheck += 1
                if usercommands is not None: 
                    cogcheck += 1
                if usermethods is not None: 
                    cogcheck += 1
                if data is not None: 
                    cogcheck += 1
                if embeds is not None: 
                    cogcheck += 1
                if events is not None: 
                    cogcheck += 1
                if logging is not None:
                    cogcheck += 1
                if utilities is not None: 
                    cogcheck += 1
                if verification is not None: 
                    cogcheck += 1

                embed.description = f"{cogcheck} of 12 cogs working."

                return embed

        except Exception as e:
            if logging is not None:
                await logging.log_error(e, 'debugmethods - cog_status', traceback.format_exc())
            
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()


def setup(bot):
    bot.add_cog(DebugMethods(bot))