from discord.bot import Bot
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.role import Role
import traceback
from typing import Union

class AdminMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def allow_role(self, role: Role, ctx: Union[ApplicationContext, Context], maxroles: int, allowbadges: bool) -> Embed :
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            
            if data is not None and verification is not None and embeds is not None:
                if verification.is_role_name_allowed(role.name) :
                    addable = await verification.is_role_addable(str(role.id), str(ctx.guild.id))
                    if addable == 1 :
                        if maxroles <= 20 :
                            if maxroles <= 0:
                                maxroles = 1

                            if await data.add_allowed_role(role.id, str(ctx.guild.id), str(ctx.author.id), maxroles, allowbadges):
                                return await embeds.generate_embed("Configuration changed", f"Exophose allowed the role `{role.name}` with id `{role.id}` to use role management commands.", 0x00CC00)
                            else:
                                return await embeds.generate_embed_unexpected_sql_error()
                        else:
                            return await embeds.generate_embed("Unable to allow role", "The maximum roles must be between 1 and 20, inclusively.")
                    elif addable == 2:
                        return await embeds.generate_embed("Unable to allow role", f"Exophose cannot allow the role `{role.name}` with id `{role.id}` as you have reached the maximum of 20 allowed roles for this guild.")
                    else :
                        if await data.update_allowed_role(ctx.guild.id, role.id, str(ctx.author.id), maxroles, allowbadges):
                            return await embeds.generate_embed("Configuration changed", f"Exophose updated the permissions for the role `{role.name}` with id `{role.id}`.", 0x00CC00)
                else:
                    return await embeds.generate_embed("Blacklisted Word", "The role you want to allow must not contain profane or offensive words.")

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'adminmethods - allow_role', traceback.format_exc())
        
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def disallow_role(self, role: Role, ctx: Union[ApplicationContext, Context]) -> Embed :
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            
            if data is not None and verification is not None and embeds is not None:
                if await verification.is_role_addable(str(role.id), str(ctx.guild.id)) == 0 :


                    logging = self.bot.get_cog("Logging")
                    if logging is not None:
                        await logging.log_event(f"User '{ctx.author.id}' disallowed role '{role.id}' in guild '{ctx.guild.id}'.", "INFO")
                    await data.delete_allowed_role_by_role(role.id)

                    return await embeds.generate_embed("Configuration changed", f"Exophose disallowed the role `{role.name}` with id `{role.id}` from using role management commands.", 0x00CC00)
                else :
                    return await embeds.generate_embed("Unable to disallow role", f"Exophose cannot disallow the role `{role.name}` with id `{role.id}` as it is already disallowed.")

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'adminmethods - disallow_role', traceback.format_exc())
            
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

def setup(bot):
    bot.add_cog(AdminMethods(bot))