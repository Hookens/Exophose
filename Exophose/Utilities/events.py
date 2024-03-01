from discord.activity import Activity
from discord.bot import Bot
from discord.enums import ActivityType
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.datahelpers import CreatedRole

NAME = "Exophose"

class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_data: bool = False, include_utilities: bool = False, include_verification: bool = False) -> tuple:
        data = self.bot.get_cog("Data") if include_data else None
        utilities = self.bot.get_cog("Utilities") if include_utilities else None
        verification = self.bot.get_cog("Verification") if include_verification else None
        
        if ((data is None and include_data) or 
            (utilities is None and include_utilities) or 
            (verification is None and include_verification)):
            raise(ValueError("One or more cogs are missing.", data, utilities, verification))
        
        return tuple(filter(None, (data, utilities, verification)))

    @commands.Cog.listener()
    @try_func_async()
    async def on_ready (self):
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_event(f"Exophose is up. {len(self.bot.cogs)} of 13 cogs running. Currently serving {len(self.bot.guilds)} servers.", "INFO")

        await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name="/help"))
        
    @commands.Cog.listener()
    @try_func_async()
    async def on_member_update(self, _, new_member: Member):
        (data, utilities, verification) = self._get_cogs(True, True, True)
        if await data.count_member_roles(new_member.guild.id, new_member.id) == 0:
            return

        if ((not await verification.has_permission(new_member.guild)) or
            new_member.guild_permissions.administrator):
            return
        
        if not await verification.user_allowed(new_member):
            while not await verification.is_user_within_max_roles(new_member.guild.id, new_member):
                await utilities.delete_role(new_member, 0)
            return

        if not await verification.is_badge_allowed(new_member.guild.id, new_member):
            created_roles: list[CreatedRole] = await data.get_member_roles(new_member.guild.id, new_member.id)
            for created_role in created_roles:
                role: Role = new_member.guild.get_role(created_role.id)
                if role is not None and role.icon is not None:
                    await role.edit(icon=None)

    @commands.Cog.listener()
    @try_func_async()
    async def on_member_remove(self, member: Member):
        (utilities,) = self._get_cogs(include_utilities=True)
        
        await utilities.delete_all_roles(member)

    @commands.Cog.listener()
    @try_func_async()
    async def on_guild_join(self, guild: Guild):
        (data,) = self._get_cogs(include_data=True)
        
        member: Member = guild.get_member(self.bot.user.id)

        for role in member.roles:
            if role.name == NAME:
                await data.add_server(role.id, guild.id)
                return

        await data.add_server('0', guild.id)

    @commands.Cog.listener()
    @try_func_async()
    async def on_guild_remove(self, guild: Guild):
        (data,) = self._get_cogs(include_data=True)
        
        if guild.name is None:
            return
        
        await data.delete_server(guild.id)

    @commands.Cog.listener()
    @try_func_async()
    async def on_guild_role_delete(self, role: Role):
        (data,) = self._get_cogs(include_data=True)
        
        if await data.is_member_role(role.id):
            await data.delete_member_role(role.id)

        if await data.is_allowed_role(role.id):
            await data.delete_allowed_role(role.id)

def setup(bot):
    bot.add_cog(Events(bot))