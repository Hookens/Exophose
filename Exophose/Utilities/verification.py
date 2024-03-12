from discord import Object
from discord.bot import Bot
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member

from Utilities.datahelpers import AllowedRole, Bundle, BundleRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data

class Verification(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def has_permission(self, guild: Guild) -> bool:
        return guild.me.guild_permissions.manage_roles

    def is_name_allowed(self, name: str) -> bool:
        lowercasewords = set(name.lower().split(' '))

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

    #Custom roles
    async def is_role_allowable(self, role_id: int, guild_id: int) -> int:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return 3
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

        for allowed_role in allowed_roles:
            if allowed_role.id == role_id:
                return 2

        if len(allowed_roles) == 20:
            return 0
        
        return 1

    async def is_user_role_addable(self, guild_id: int, member: Member) -> bool:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return False
        
        created_count: int = await data.count_member_roles(guild_id, member.id)

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

        if created_count < highest:
            return True
        
        return False

    async def is_user_within_max_roles(self, guild_id: int, member: Member) -> bool:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return False
        
        created_count: int = await data.count_member_roles(guild_id, member.id)

        if created_count == 0:
            return True
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

        highest: int = 0
        for allowed_role in allowed_roles:
            for role in member.roles:
                if role.id == allowed_role.id:
                    if (max_roles := allowed_role.max_roles) > highest:
                        highest = max_roles
                    break

        if created_count > highest:
            return False
            
        return True

    async def is_user_allowed(self, member: Member) -> bool:
        if member.guild_permissions.administrator: 
            return True
        
        for role in member.roles:
            if await self.is_role_allowable(role.id, member.guild.id) == 2:
                return True

        return False

    async def is_badge_allowed(self, guild_id: int, member: Member) -> bool:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return False
        
        allowed: bool = False
        
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

    #Bundles
    async def is_bundle_role_addable(self, role_id: int, guild_id: int, index: int) -> int:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return 3
        
        bundle: Bundle = await data.get_bundle(guild_id, index)
        bundle_roles: list[AllowedRole] = await data.get_bundle_roles(bundle.id)

        for bundle_role in bundle_roles:
            if bundle_role.id == role_id:
                return 0

        if len(bundle_roles) == 10:
            return 2
        
        return 1
    
    async def is_bundle_allowed_role_allowable(self, role_id: int, guild_id: int, index: int) -> int:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return 3
        
        bundle: Bundle = await data.get_bundle(guild_id, index)
        allowed_roles: list[AllowedRole] = await data.get_bundle_allowed_roles(bundle.id)

        for allowed_role in allowed_roles:
            if allowed_role.id == role_id:
                return 0

        if len(allowed_roles) == 5:
            return 2
        
        return 1

    async def is_bundle_selection_valid(self, guild_id: int, index: int, name: str) -> bool:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return False
        
        bundle_name = (await data.get_bundle(guild_id, index)).name

        return name == bundle_name

    async def get_allowed_bundle_roles(self, member: Member) -> list[BundleRole]:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return None
        
        allowed_bundle_roles: list[BundleRole] = list()
        allowed_guild_roles: list[BundleRole] = await data.get_allowed_bundle_roles(member.guild.id)

        for allowed_guild_role in allowed_guild_roles:
            for role in member.roles:
                if role.id == allowed_guild_role.id:
                    allowed_bundle_roles.append(allowed_guild_role)
                    break

        return allowed_bundle_roles

    async def check_user_bundle_roles(self, allowed_roles: list[BundleRole], member: Member, remove_all: bool = False) -> bool:
        data: 'Data' = self.bot.get_cog("Data")
        if data is None:
            return False
        
        if member.guild_permissions.administrator:
            return True
        
        bundle_roles: list[int] = await data.get_bundles_roles(member.guild.id)
        bundle_allowed_roles: list[int] = await data.get_bundles_choices(allowed_roles)

        if not bundle_allowed_roles:
            return False
        
        roles_to_remove = bundle_roles if remove_all else list(set(bundle_roles) - set(bundle_allowed_roles))
        member_roles_to_remove = []
        for member_role in member.roles:
            if member_role.id in roles_to_remove:
                member_roles_to_remove.append(member_role.id)
        roles = [Object(role) for role in member_roles_to_remove]
        
        try:
            await member.remove_roles(*roles, reason="Bundle role management")
        except:
            pass
                    
        return True




def setup(bot):
    bot.add_cog(Verification(bot))