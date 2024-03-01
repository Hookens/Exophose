from discord.bot import Bot
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member

from Utilities.datahelpers import AllowedRole, CreatedRole

class Verification(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def is_role_name_allowed(self, rolename: str) -> bool:
        lowercasewords = set(rolename.lower().split(' '))

        with open("Exophose/bannedwords.txt", "r") as file:
            bannedcontained = set()
            bannedexact = set()

            for line in file:
                if line.startswith("*"):
                    bannedcontained.add(line[1:].strip())
                else:
                    bannedexact.add(line.strip())

            if any(lowercasewords & bannedexact) or any(word1 in word2 for word1 in bannedcontained for word2 in lowercasewords):
                return False
            
        return True

    async def is_role_allowable(self, role_id: int, guild_id: int) -> int:
        if (data := self.bot.get_cog("Data")) is None:
            return 3
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

        if len(allowed_roles) == 20:
            return 0

        for allowed_role in allowed_roles:
            if allowed_role.id == role_id:
                return 2
        
        return 1

    async def is_user_role_addable(self, guild_id: int, member: Member) -> bool:
        if (data := self.bot.get_cog("Data")) is None:
            return False
        
        created_roles: list[CreatedRole] = await data.get_member_roles(guild_id, member.id)

        highest: int = 0

        if member.guild_permissions.administrator:
            highest = 20

        else:
            allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

            for allowed_role in allowed_roles:
                for role in member.roles:
                    if role.id == allowed_role.id:
                        if (max_roles := allowed_role.max_roles) > highest:
                            highest = max_roles
                        break

        if len(created_roles) < highest:
            return True
        
        return False

    async def is_user_within_max_roles(self, guild_id: int, member: Member) -> bool:
        if (data := self.bot.get_cog("Data")) is None:
            return False
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)
        created_roles: list[CreatedRole] = await data.get_member_roles(guild_id, member.id)

        highest: int = 0
        for allowed_role in allowed_roles:
            for role in member.roles:
                if role.id == allowed_role.id:
                    if (max_roles := allowed_role.max_roles) > highest:
                        highest = max_roles
                    break

        if len(created_roles) > highest:
            return False
            
        return True

    async def user_allowed(self, member: Member) -> bool:
        if member.guild_permissions.administrator: 
            return True
        
        for role in member.roles:
            if await self.is_role_allowable(role.id, member.guild.id) == 2:
                return True

        return False

    async def has_permission(self, guild: Guild) -> bool:
        return guild.me.guild_permissions.manage_roles

    async def is_badge_allowed(self, guild_id: int, member: Member) -> bool:
        data = self.bot.get_cog("Data")
        allowed: bool = False

        if data is None:
            return
        
        if member.guild_permissions.administrator:
            allowed = True
        else:
            allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

            for allowed_role in allowed_roles:
                for role in member.roles:
                    if role.id == allowed_role.id:
                        allowed = allowed_role
                        break
                if allowed:
                    break

        return allowed

def setup(bot):
    bot.add_cog(Verification(bot))