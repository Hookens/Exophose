from discord.bot import Bot
from discord.channel import TextChannel
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member
from discord.role import Role
import re

class Verification(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def is_role_name_allowed(self, rolename: str) -> bool :
        """Checks if a role name contains profane or offensive words.\n
        Returns: The boolean representing whether or not it does."""

        file = open("Exophose/bannedwords.txt", "r")
        lines = file.readlines()

        bannedcontained = []
        bannedexact = []

        loweracsewords = rolename.lower().split(' ')

        for line in lines :
            if line[0] == '1' :
                bannedcontained.append(line[1:].strip("\n"))
            else:
                bannedexact.append(line[1:].strip("\n"))

        for word in loweracsewords :
            for exact in bannedexact :
                if exact == word :
                    file.close()
                    return False
            for contained in bannedcontained :
                if contained in word :
                    file.close()
                    return False

        file.close()
        return True

    def has_channel_permission(self, guild: Guild, channel: TextChannel, permission: int) -> bool:
        member: Member = guild.get_member(self.bot.user.id)

        if permission == 1:
            return channel.permissions_for(member).send_messages
        elif permission == 2:
            return channel.permissions_for(member).embed_links

    async def is_role_addable(self, roleid: str, guildid: str) -> int:
        """Checks if a specific role is present within the list of allowed roles, using the role ID.\n
        Returns: A boolean representing whether or not the role is present."""

        data = self.bot.get_cog("Data")
        if data is not None:
            guildallowedroles = await data.get_allowed_roles_by_guild(guildid)

            for allowedrole in guildallowedroles:
                if allowedrole[1] == roleid:
                    return 0

            if len(guildallowedroles) == 20:
                return 2
            
            return 1

    async def is_user_role_addable(self, guildid: str, member: Member) -> bool :
        """Checks if a user is allowed to create themselves a role, using the guild ID and user ID.\n
        Returns: A boolean representing whether or not they can create it."""
        
        data = self.bot.get_cog("Data")
        if data is not None:
            usercreatedroles = await data.get_created_roles_by_guild_by_user(guildid, member._user.id)

            highest: int = 0


            if member.guild_permissions.administrator:
                highest = 20

            else:
                guildallowedroles = await data.get_allowed_roles_by_guild(guildid)

                for allowedrole in guildallowedroles:
                    for role in member.roles:
                        if role.id == int(allowedrole[1]) :
                            if int(allowedrole[4]) > highest:
                                highest = int(allowedrole[4])
                        continue

            if len(usercreatedroles) < highest:
                return True

        return False

    async def is_user_within_maxroles(self, guildid: str, member: Member) -> bool :
        """Checks if a user is allowed to create themselves a role, using the guild ID and user ID.\n
        Returns: A boolean representing whether or not they can create it."""

        data = self.bot.get_cog("Data")
        if data is not None:
            guildallowedroles = await data.get_allowed_roles_by_guild(guildid)

            usercreatedroles = await data.get_created_roles_by_guild_by_user(guildid, member._user.id)

            highest: int = 0
            for allowedrole in guildallowedroles:
                for role in member.roles:
                    if role.id == int(allowedrole[1]) :
                        if int(allowedrole[4]) > highest:
                            highest = int(allowedrole[4])
                        break

            if len(usercreatedroles) > highest:
                return False
            
        return True

    async def user_allowed(self, member: Member) -> bool :
        """Checks if a specific guild member is allowed to use the bot's commands.\n
        Returns: A boolean representing whether or not the user is allowed."""

        try:
            if member.guild_permissions.administrator: 
                return True
            
            else :
                for role in member.roles :
                    if await self.is_role_addable(str(role.id), str(member.guild.id)) == 0 :
                        return True
            return False
            
        except Exception as e:
            #await log_error(e, "Exophose", 'verification - user_allowed', traceback.format_exc())
            return False

    async def has_permission(self, guild: Guild, permission: int) -> bool:
        
        data = self.bot.get_cog("Data")
        if data is not None:
            id: int = await data.get_exophose_role_by_guild(guild.id)
            
            if id != 0:
                botRole: Role = guild.get_role(id)

                if permission == 0:
                    return botRole.permissions.manage_roles
                elif permission == 1:
                    return botRole.permissions.send_messages
                else:
                    return botRole.permissions.embed_links
            else:
                bot: Member = guild.me

                if permission == 0:
                    return bot.guild_permissions.manage_roles
                elif permission == 1:
                    return bot.guild_permissions.send_messages
                else:
                    return bot.guild_permissions.embed_links

        return False

    async def is_badge_allowed(self, guildid: str, member: Member) -> bool:
        data = self.bot.get_cog("Data")
        allowed: bool = False

        if data is not None:
            if member.guild_permissions.administrator:
                allowed = True
            else:
                guildallowedroles = await data.get_allowed_roles_by_guild(guildid)

                for allowedrole in guildallowedroles:
                    for role in member.roles:
                        if role.id == int(allowedrole[1]) :
                            if bool(allowedrole[8]):
                                allowed = True
                            break

        return allowed

    def is_badge_link_allowed(self, link: str) -> bool:
        return re.match("^https:\/\/(cdn\.discordapp\.com|media\.discordapp\.net)\/.*(\.jpg|.jpeg|.png)$", link) is not None

def setup(bot):
    bot.add_cog(Verification(bot))