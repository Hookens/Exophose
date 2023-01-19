from discord.bot import Bot
from discord.colour import Colour
from discord.commands.context import ApplicationContext
from discord.embeds import Embed
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.commands import Context
from discord.guild import Guild
from discord.member import Member
from discord.role import Role
import traceback
from typing import Union

class UserMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def role_create (self, ctx: Union[ApplicationContext, Context], rolename: str, rolecolor: str, rolebadge: str = None) -> Embed:
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and verification is not None and embeds is not None and utilities is not None:
                if await verification.has_permission(ctx.guild, 0):
                    if await verification.is_user_role_addable(ctx.guild.id, ctx.author) :

                        if verification.is_role_name_allowed(rolename) :

                            hexcolor = await utilities.parse_color(rolecolor)

                            if hexcolor is not None :
                                createdRole: Role = await ctx.guild.create_role(name=rolename,colour=Colour(hexcolor))
                                if await data.add_created_role(str(createdRole.id), str(ctx.guild.id), str(ctx.author.id)):
                                    await ctx.author.add_roles(createdRole)
                                    await utilities.reposition(createdRole)
                                    embed: Embed = await embeds.generate_embed("Role creation success", f"Exophose successfully created your new role.", 0x00CC00)

                                    if rolebadge is not None:
                                        if "ROLE_ICONS" in ctx.guild.features:
                                            if await verification.is_badge_allowed(ctx.guild.id, ctx.author):
                                                if "?" in rolebadge:
                                                    rolebadge = rolebadge.split("?")[0]
                                                if verification.is_badge_link_allowed(rolebadge):
                                                    badge: bytes = await utilities.fetch_image(rolebadge)
                                                    if badge is not None:
                                                        await createdRole.edit(icon=badge)
                                                    else:
                                                        embed.set_footer(text="The link you have provided was valid but Exophose could not access it.")
                                                else:
                                                    embed.set_footer(text="The link you have provided is invalid. Make sure it's a `cdn.discordapp.com` or `media.discordapp.net` link.")
                                            else:
                                                embed.set_footer(text="You do not have badge permissions with your currently allowed role(s).")
                                        else:
                                            embed.set_footer(text="Your guild does not support custom role badges.")

                                    return embed

                                else:
                                    await createdRole.delete(reason="Impossible to connect to the SQL database at the moment.")
                                    return await embeds.generate_embed_unexpected_sql_error()
                            else :
                                return await embeds.generate_embed_color_parsing_error(rolecolor)
                        else:
                            return await embeds.generate_embed("Blacklisted Word", "Your role name must not contain profane or offensive words.")
                    else:
                        return await embeds.generate_embed("Maximum Roles", "You have reached the maximum number of roles for your allowed role.")
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_create', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_create', traceback.format_exc())

        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def role_remove (self, member: Member, roleindex) -> Embed:
        try:
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            
            if verification is not None and embeds is not None:
                if await verification.has_permission(member.guild, 0):
                    if await self.role_delete(member, roleindex):
                        return await embeds.generate_embed("Role removal success", f"Exophose successfully removed your role(s).", 0x00CC00)
                    else:
                        return await embeds.generate_embed("Role removal impossible", f"Exophose cannot remove your custom role, as you do not have one, or the provided index is invalid.")
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_remove', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_remove', traceback.format_exc())
        
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def role_recolor (self, ctx: Union[ApplicationContext, Context], rolecolor: str, roleindex: int) -> Embed:
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and verification is not None and embeds is not None and utilities is not None:
                if await verification.has_permission(ctx.guild, 0):
                    hexcolor = await utilities.parse_color(rolecolor)

                    if hexcolor:
                        usercreatedroles = await data.get_created_roles_by_guild_by_user(ctx.guild.id,ctx.author._user.id)

                        if len(usercreatedroles) > 0:
                            if roleindex is None and len(usercreatedroles) > 1:
                                return await embeds.generate_embed("Role recolor error", "You must specify the index of the role you want to recolor as you have more than one.")
                            else:
                                if roleindex < len(usercreatedroles) and roleindex >= 0:
                                    role: Role = ctx.guild.get_role(int(usercreatedroles[roleindex][1]))
                                    await role.edit(colour=Colour(hexcolor))
                                    return await embeds.generate_embed_success_modification("recolor")
                                else:
                                    return await embeds.generate_embed_fail_index_modification("recolor")
                        else:
                            return await embeds.generate_embed_fail_missing_modification("recolor")
                    else :
                        return await embeds.generate_embed_color_parsing_error(rolecolor)
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_recolor', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_recolor', traceback.format_exc())

        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def role_rename (self, ctx: Union[ApplicationContext, Context], rolename: str, roleindex: int) -> Embed:
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and verification is not None and embeds is not None and utilities is not None:
                if await verification.has_permission(ctx.guild, 0):

                    if verification.is_role_name_allowed(rolename) :
                            
                        usercreatedroles = await data.get_created_roles_by_guild_by_user(ctx.guild.id,ctx.author._user.id)

                        if len(usercreatedroles) > 0:
                            if roleindex is None and len(usercreatedroles) > 1:
                                return await embeds.generate_embed("Missing arguments", "You must specify the index of the role you want to rename as you have more than one.")
                            else:
                                if roleindex < len(usercreatedroles) and roleindex >= 0:
                                    role: Role = ctx.guild.get_role(int(usercreatedroles[roleindex][1]))
                                    await role.edit(name=rolename)
                                    return await embeds.generate_embed_success_modification("rename")
                                else:
                                    return await embeds.generate_embed_fail_index_modification("rename")
                        else:
                            return await embeds.generate_embed_fail_missing_modification("rename")
                    else:
                        return await embeds.generate_embed("Blacklisted Word", "Your role name must not contain profane or offensive words.")
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_rename', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_rename', traceback.format_exc())
        
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def role_rebadge (self, ctx: Union[ApplicationContext, Context], rolebadge: str, roleindex: int) -> Embed:
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and verification is not None and embeds is not None and utilities is not None:
                if await verification.has_permission(ctx.guild, 0):

                    if await verification.is_badge_allowed(ctx.guild.id, ctx.author):
                        if "?" in rolebadge:
                            rolebadge = rolebadge.split("?")[0]

                        usercreatedroles = await data.get_created_roles_by_guild_by_user(ctx.guild.id,ctx.author._user.id)

                        if len(usercreatedroles) > 0:
                            if roleindex is None and len(usercreatedroles) > 1:
                                return await embeds.generate_embed("Missing arguments", "You must specify the index of the role you want to rebadge as you have more than one.")
                            else:
                                if roleindex < len(usercreatedroles) and roleindex >= 0:
                                    role: Role = ctx.guild.get_role(int(usercreatedroles[roleindex][1]))
                                    
                                    
                                    if rolebadge.lower().strip() == "none":
                                        await role.edit(icon=None)

                                    elif verification.is_badge_link_allowed(rolebadge):
                                        badge: bytes = await utilities.fetch_image(rolebadge)
                                        if badge is not None:
                                            await role.edit(icon=badge)
                                        else:
                                            return await embeds.generate_embed_link_error()
                                    else:
                                        return await embeds.generate_embed_not_link_allowed()
                                        
                                    return await embeds.generate_embed_success_modification("rebadge")
                                else:
                                    return await embeds.generate_embed_fail_index_modification("rebadge")
                        else:
                            return await embeds.generate_embed_fail_missing_modification("rebadge")
                    else:
                        return await embeds.generate_embed_not_badge_allowed()
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_rebadge', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_rebadge', traceback.format_exc())
        
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()

    async def role_reposition (self, ctx: Union[ApplicationContext, Context], roleindex: int) -> Embed :
        try:
            data = self.bot.get_cog("Data")
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and verification is not None and embeds is not None and utilities is not None:
                if await verification.has_permission(ctx.guild, 0):
                    usercreatedroles = await data.get_created_roles_by_guild_by_user(ctx.guild.id,ctx.author._user.id)

                    if len(usercreatedroles) > 1:
                        if roleindex is None:
                            return await embeds.generate_embed("Missing arguments", "You must specify the index of the role you want to reposition above your other ones.")
                        else:
                            roleindexint: int = -1
                            if utilities.parsable_int(roleindex):
                                roleindexint = int(roleindex)
                            
                                if roleindexint < len(usercreatedroles) and roleindexint >= 0:
                                    role: Role = ctx.guild.get_role(int(usercreatedroles[roleindexint][1]))
                                    await utilities.reposition(role)
                                    return await embeds.generate_embed_success_modification("reposition")
                                else:
                                    return await embeds.generate_embed_fail_index_modification("reposition")
                    else:
                        return await embeds.generate_embed_fail_missing_modification("reposition")
                else:
                    return await embeds.generate_embed_missing_permissions(0)

        except HTTPException as e:
            if e.code == 403:
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_error(e, 'usermethods - role_reposition', traceback.format_exc())
                if embeds is not None:
                    return await embeds.generate_embed_forbidden_error()

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_reposition', traceback.format_exc())
        
        if embeds is not None:
            return await embeds.generate_embed_unexpected_error()
        
        return embeds
    
    async def role_delete(self, member: Member, roleindex) -> bool:
        try:
            data = self.bot.get_cog("Data")
            utilities = self.bot.get_cog("Utilities")
            
            if data is not None and utilities is not None:
                usercreatedroles = await data.get_created_roles_by_guild_by_user(member.guild.id, member._user.id)

                if len(usercreatedroles) > 0 :
                    if type(roleindex) is str and roleindex.lower().strip() == "all":
                        logging = self.bot.get_cog("Logging")
                        if logging is not None:
                            await logging.log_event(f"User '{member.id}' removed all of their roles in guild '{member.guild.id}'.", "INFO")
                        if await data.delete_created_roles_by_guild_by_user(member.guild.id, member._user.id):
                            for usercreatedrole in usercreatedroles :
                                guild: Guild = self.bot.get_guild(int(usercreatedrole[2]))
                                role: Role = guild.get_role(int(usercreatedrole[1]))
                                await role.delete()
                            return True

                    else :
                        if utilities.parsable_int(roleindex):
                            roleindexint = int(roleindex)
                            if roleindexint < len(usercreatedroles) and roleindexint >= 0:

                                guild: Guild = self.bot.get_guild(int(usercreatedroles[roleindexint][2]))
                                role: Role = guild.get_role(int(usercreatedroles[roleindexint][1]))

                                
                                logging = self.bot.get_cog("Logging")
                                if logging is not None:
                                    await logging.log_event(f"User '{member.id}' removed role '{role.id}' in guild '{member.guild.id}'.", "INFO")
                                if await data.delete_created_role_by_role(role.id):
                                    await role.delete()
                                    return True

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usermethods - role_delete', traceback.format_exc())
        
        return False

def setup(bot):
    bot.add_cog(UserMethods(bot))