from discord.bot import Bot
from discord.ext import commands
from mysql import connector
import os

from Utilities.datahelpers import ExoRole, CreatedRole, AllowedRole

HOST = os.getenv('DATABASE_HST')
USER = os.getenv('DATABASE_USR')
PASSWORD = os.getenv('DATABASE_PWD')
DATABASE = USER

DB_CONFIG = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
}


class Data(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
    def _get_db_connection(self):
        return connector.connect(**DB_CONFIG)
    
    async def _log_sql_event(self, event: str, type: str):
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_event(event, type)
    
    async def _log_sql_error(self, e: Exception, method: str, *args):
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_error("'SQLError'", f"Data - {method}", e, *args)

    async def _execute_write_operation(self, proc_name: str, *args) -> bool:
        try:
            with self._get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.callproc(proc_name, args)
                    connection.commit()
                    return True
                
        except Exception as e:
            await self._log_sql_error(e, proc_name, *args)
            return False

    async def _execute_read_operation(self, proc_name: str, *args):
        try:
            with self._get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.callproc(proc_name, args)
                    for result in cursor.stored_results():
                        allowed_roles=result.fetchall()
                    return allowed_roles
                
        except Exception as e:
            await self._log_sql_error(e, proc_name, *args)
            return None

    async def add_server(self, role_id: int, guild_id: int) -> bool:
        await self._log_sql_event(f"'{guild_id}' added with '{role_id}'", "INFO")
        return await self._execute_write_operation("ExoAddServer", role_id, guild_id)

    async def add_allowed_role(self, role_id: int, guild_id: int, user_id: int, max_roles:int, allow_badges: bool) -> bool:
        await self._log_sql_event(f"'{user_id}' from '{guild_id}' allowed '{role_id}' ({max_roles}, {allow_badges})", "INFO")
        return await self._execute_write_operation("ExoAddAllowedRole", role_id, guild_id, user_id, max_roles, allow_badges)

    async def add_member_role(self, role_id: int, guild_id: int, user_id: int) -> bool:
        await self._log_sql_event(f"'{user_id}' from '{guild_id}' created '{role_id}'", "INFO")
        return await self._execute_write_operation("ExoAddMemberRole", role_id, guild_id, user_id)
    
    async def is_allowed_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsAllowedRole", role_id))[0][0])
    
    async def is_member_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsMemberRole", role_id))[0][0])
    
    async def count_member_roles(self, guild_id: int, user_id: int) -> int:
        return int((await self._execute_read_operation("ExoCountMemberRoles", guild_id, user_id))[0][0])

    async def get_server(self, guild_id: int) -> ExoRole:
        result = await self._execute_read_operation("ExoGetServer", guild_id)
        return ExoRole(
            id=result[0][0],
            guild_id=result[0][1]
            ) if result is not None else None

    async def get_allowed_roles(self, guild_id: int) -> list[AllowedRole]:
        result = await self._execute_read_operation("ExoGetAllowedRoles", guild_id)
        return [AllowedRole(
            id=row[0],
            guild_id=row[1],
            user_id=row[2],
            max_roles=row[3],
            allow_badges=row[7],
            created_date=row[4],
            updated_user_id=row[5],
            updated_date=row[6]
            ) for row in result] if result is not None else None

    async def get_member_roles(self, guild_id: int, user_id: int) -> list[CreatedRole]:
        result = await self._execute_read_operation("ExoGetMemberRoles", guild_id, user_id)
        return [CreatedRole(
            id=row[0],
            guild_id=row[1],
            user_id=row[2],
            created_date=row[3],
            ) for row in result] if result is not None else None

    async def delete_server(self, guild_id: int) -> bool:
        await self._log_sql_event(f"Removed from '{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteServer", guild_id)

    async def delete_allowed_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed allowed '{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteAllowedRole", role_id)

    async def delete_member_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed created '{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteMemberRole", role_id)

    async def delete_member_roles(self, guild_id: int, user_id: int) -> bool:
        await self._log_sql_event(f"Removed '{user_id}' from '{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteMemberRoles", guild_id, user_id)
    
def setup(bot):
    bot.add_cog(Data(bot))