from calendar import c
from discord.activity import Activity
from discord.bot import Bot
from discord.channel import DMChannel
from discord.enums import ActivityType
from discord.ext import commands
from discord.ext.commands import Context
from discord.guild import Guild
from discord.member import Member
from discord.role import Role
import traceback

class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        try:
            cogcheck: int = 1
            
            data = self.bot.get_cog("Data")
            if data is not None:
                cogcheck += 1
                await data.reconnect()

            logging = self.bot.get_cog("Logging")
            if logging is not None:
                cogcheck += 1

            if self.bot.get_cog("Embeds") is not None:
                cogcheck += 1
            if self.bot.get_cog("Utilities") is not None:
                cogcheck += 1
            if self.bot.get_cog("Verification") is not None:
                cogcheck += 1
            if self.bot.get_cog("DebugMethods") is not None:
                cogcheck += 1
            if self.bot.get_cog("DebugCommands") is not None:
                cogcheck += 1
            if self.bot.get_cog("AdminMethods") is not None:
                cogcheck += 1
            if self.bot.get_cog("AdminCommands") is not None:
                cogcheck += 1
            if self.bot.get_cog("UserMethods") is not None:
                cogcheck += 1
            if self.bot.get_cog("UserCommands") is not None:
                cogcheck += 1
            
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="/help"))
            
            if logging is not None:
                await logging.log_event(f"Exophose is up. {cogcheck} of 12 cogs running. Currently serving {len(self.bot.guilds)} servers.", "INFO")

        except Exception as e:
            if logging is not None:
                await logging.log_error(e,'events - on_ready', traceback.format_exc())
        
        return
        
    @commands.Cog.listener()
    async def on_member_update(self, oldMember: Member, newMember: Member):
        try:
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            data = self.bot.get_cog("Data")
            
            if verification is not None and methods is not None:
                if await verification.has_permission(newMember.guild, 0):
                    if not await verification.user_allowed(newMember):
                        await methods.role_delete(newMember, "all")
                    else:
                        if not newMember.guild_permissions.administrator:
                            if not await verification.is_user_within_maxroles(newMember.guild.id, newMember):
                                await methods.role_delete(newMember, 0)

                            if data is not None:
                                if not await verification.is_badge_allowed(newMember.guild.id, newMember):
                                    for row in await data.get_created_roles_by_guild_by_user(newMember.guild.id, newMember.id):
                                        role: Role = newMember.guild.get_role((int)(row[1]))
                                        if role is not None and role.icon is not None:
                                            await role.edit(icon=None)
                                        

            
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'events - on_member_update', traceback.format_exc())
        
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        try:
            methods = self.bot.get_cog("UserMethods")
            
            if methods is not None:
                await methods.role_delete(member, "all")

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'events - on_member_remove', traceback.format_exc())
        
        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        try:
            data = self.bot.get_cog("Data")
            
            if data is not None:
                member: Member = guild.get_member(self.bot.user.id)

                for role in member.roles:
                    if role.name == 'Exophose':
                        await data.add_exophose_role(role.id, guild.id)
                        return

                await data.add_exophose_role('0', guild.id)
            
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'events - on_guild_join', traceback.format_exc())
        
        return

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        try:
            data = self.bot.get_cog("Data")
            
            if data is not None:
                if guild.name is not None:
                    logging = self.bot.get_cog("Logging")
                    if logging is not None:
                        await logging.log_event(f"Exophose was removed from guild '{guild.id}'.", "INFO")
                    await data.delete_created_roles_by_guild(guild.id)
                    await data.delete_allowed_roles_by_guild(guild.id)
                    await data.delete_exophose_role_by_guild(guild.id)
            
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'events - on_guild_remove', traceback.format_exc())
        
        return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: Role):
        try:
            data = self.bot.get_cog("Data")
            
            if data is not None:
                await data.delete_created_role_by_role(role.id)
                await data.delete_allowed_role_by_role(role.id)
            
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'events - on_guild_role_delete', traceback.format_exc())
        
        return

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, e):
        embeds = self.bot.get_cog("Embeds")
        if embeds is not None:
            if type(ctx.channel) is not DMChannel:
                if isinstance(e, commands.CommandNotFound):
                    await ctx.send(embed = await embeds.generate_embed("Command not found", "For a list of commands, enter `exo help` or use `/help`."))
                elif isinstance(e, commands.MemberNotFound):
                    await ctx.send(embed = await embeds.generate_embed("Member not found", "The input you have provided is not a valid member."))
                elif isinstance(e, commands.RoleNotFound):
                    await ctx.send(embed = await embeds.generate_embed("Role not found", "The input you have provided is not a valid role."))

def setup(bot):
    bot.add_cog(Events(bot))