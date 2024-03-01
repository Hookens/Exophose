from discord.bot import Bot
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member
from discord.role import Role

from Debug.debughelpers import try_func_async
from Utilities.datahelpers import ExoRole, CreatedRole

class Utilities(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cog(self):
        data = self.bot.get_cog("Data")
        
        if data is None:
            raise(ValueError("Data cog missing."))

        return data

    def parsable_color(self, color: str) -> bool:
        try:
            intcolor: int = int(color, 16)
        except:
            return False
        
        return True

    @try_func_async()
    async def parse_color(self, color: str):
        hexcolor = color.replace('#', '')

        if not self.parsable_color(hexcolor):
            return 0
        
        intcolor = int(hexcolor, 16)
        if intcolor > 0xFFFFFF or intcolor < 0:
            intcolor = 0
        elif intcolor == 0:
            intcolor = 0x010101
        
        return intcolor

    @try_func_async()
    async def reposition(self, role: Role):
        data = self._get_cog()
        
        exo_role: ExoRole = await data.get_server(role.guild.id)
        
        if exo_role is None or exo_role.id == 0:
            return
        
        botrole = role.guild.get_role(exo_role.id)

        if botrole and botrole.permissions.manage_roles:
            try:
                await role.edit(position=botrole.position - 1)
            except:
                pass

    @try_func_async()
    async def delete_role(self, member: Member, role_index: int) -> bool:
        data = self._get_cog()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.guild.id, member.id)

        if 0 <= role_index < len(created_roles):
            guild: Guild = self.bot.get_guild(created_roles[role_index].guild_id)
            role: Role = guild.get_role(created_roles[role_index].id)

            if await data.delete_member_role(role.id):
                await role.delete()
                return True
            
        return False

    @try_func_async()
    async def delete_all_roles(self, member: Member):
        data = self._get_cog()

        if not any(member.roles):
            return
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.guild.id, member.id)
        if not any(created_roles):
            return
        
        await data.delete_member_roles(member.guild.id, member.id)

        for created_role in created_roles:
            guild: Guild = self.bot.get_guild(created_role.guild_id)
            role: Role = guild.get_role(created_role.id)
            
            await role.delete()

def setup(bot):
    bot.add_cog(Utilities(bot))