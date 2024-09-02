from discord.bot import Bot
from discord.ext import commands
from mysql import connector
import os

from Utilities.constants import Env
from Utilities.datahelpers import Bundle, BundleRole, ExoRole, CreatedRole, AllowedRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.logging import Logging

HOST = os.getenv(Env.DBHST)
USER = os.getenv(Env.DBUSR)
PASSWORD = os.getenv(Env.DBPWD)
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
        logging: 'Logging'
        if (logging := self.bot.get_cog("Logging")) is not None:
            await logging.log_event(event, type)
    
    async def _log_sql_error(self, e: Exception, method: str, *args):
        logging: 'Logging'
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


    #Custom roles
    async def add_server(self, role_id: int, guild_id: int) -> bool:
        await self._log_sql_event(f"Joined G'{guild_id}' with R'{role_id}'", "INFO")
        return await self._execute_write_operation("ExoAddServer", role_id, guild_id)

    async def add_allowed_role(self, role_id: int, guild_id: int, user_id: int, max_roles:int, allow_badges: bool) -> bool:
        await self._log_sql_event(f"Allowed R'{role_id}' ({max_roles}, {allow_badges}) from G'{guild_id}' by U'{user_id}'", "INFO")
        return await self._execute_write_operation("ExoAddAllowedRole", role_id, guild_id, user_id, max_roles, allow_badges)

    async def add_member_role(self, role_id: int, guild_id: int, user_id: int) -> bool:
        await self._log_sql_event(f"Created R'{role_id}' from G'{guild_id}' by U'{user_id}'", "INFO")
        return await self._execute_write_operation("ExoAddMemberRole", role_id, guild_id, user_id)
    
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
        await self._log_sql_event(f"Removed from G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteServer", guild_id)

    async def delete_allowed_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed allowed R'{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteAllowedRole", role_id)

    async def delete_member_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed created R'{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteMemberRole", role_id)

    async def delete_member_roles(self, guild_id: int, user_id: int) -> bool:
        await self._log_sql_event(f"Removed U'{user_id}' from G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteMemberRoles", guild_id, user_id)
    
    async def is_allowed_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsAllowedRole", role_id))[0][0])
    
    async def is_member_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsMemberRole", role_id))[0][0])
    
    async def count_member_roles(self, guild_id: int, user_id: int) -> int:
        return int((await self._execute_read_operation("ExoCountMemberRoles", guild_id, user_id))[0][0])


    #Bundles
    async def add_bundle(self, guild_id: int, name: str) -> bool:
        await self._log_sql_event(f"Bundle '{name}' added in G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoAddBundle", guild_id, name)

    async def add_bundle_allowed_role(self, role_id: int, guild_id: int, index: int) -> bool:
        await self._log_sql_event(f"Bundle '{index}' allowed R'{role_id}' in G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoAddBundleAllowedRole", role_id, guild_id, index)
    
    async def add_bundle_role(self, role_id: int, guild_id: int, index: int) -> bool:
        await self._log_sql_event(f"Bundle '{index}' added R'{role_id}' in G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoAddBundleRole", role_id, guild_id, index)

    async def get_bundle(self, guild_id: int, index: int) -> Bundle:
        result = await self._execute_read_operation("ExoGetBundle", guild_id, index)
        return Bundle(
            id=result[0][0],
            guild_id=result[0][1],
            name=result[0][2]
            ) if result is not None else None

    async def get_bundles(self, guild_id: int) -> list[Bundle]:
        result = await self._execute_read_operation("ExoGetBundles", guild_id)
        return [Bundle(
            id=row[0],
            guild_id=row[1],
            name=row[2]
            ) for row in result] if result is not None else None
    
    async def get_bundle_allowed_roles(self, bundle_id: int) -> list[BundleRole]:
        result = await self._execute_read_operation("ExoGetBundleAllowedRoles", bundle_id)
        return [BundleRole(
            bundle_id=row[0],
            id=row[1],
            guild_id=row[2],
            ) for row in result] if result is not None else None
    
    async def get_bundle_roles(self, bundle_id: int) -> list[BundleRole]:
        result = await self._execute_read_operation("ExoGetBundleRoles", bundle_id)
        return [BundleRole(
            bundle_id=row[0],
            id=row[1],
            guild_id=row[2],
            ) for row in result] if result is not None else None

    async def get_bundles_roles(self, guild_id: int) -> list[int]:
        result = await self._execute_read_operation("ExoGetBundlesRoles", guild_id)
        return [int(row[0]) for row in result] if result is not None else None

    async def get_bundles_choices(self, allowed_roles: list[BundleRole]) -> list[int]:
        if not allowed_roles:
            return []

        distinct_bundles: list[int] = list(set(role.bundle_id for role in allowed_roles))
        bundle_roles: list[BundleRole] = list()

        for bundle_id in distinct_bundles:
            bundle_roles.extend(await self.get_bundle_roles(bundle_id))

        return list(set(role.id for role in bundle_roles))
    
    async def get_bundles_choice(self, allowed_roles: list[BundleRole], index: int) -> int:
        choices = await self.get_bundles_choices(allowed_roles)
        return choices[index]

    async def get_allowed_bundle_roles(self, guild_id: int) -> list[BundleRole]:
        result = await self._execute_read_operation("ExoGetAllowedBundleRoles", guild_id)
        return [BundleRole(
            bundle_id=row[0],
            id=row[1],
            guild_id=row[2],
            ) for row in result] if result is not None else None

    async def delete_bundle(self, guild_id: int, index: int) -> bool:
        await self._log_sql_event(f"Bundle '{index}' removed from G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteBundle", guild_id, index)

    async def delete_bundle_allowed_role(self, role_id: int, guild_id: int, index: int) -> bool:
        await self._log_sql_event(f"Bundle '{index}' disallowed R'{role_id}' in G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteBundleAllowedRole", role_id, guild_id, index)

    async def delete_bundle_role(self, role_id: int, guild_id: int, index: int) -> bool:
        await self._log_sql_event(f"Bundle '{index}' removed R'{role_id}' in G'{guild_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteBundleRole", role_id, guild_id, index)
    
    async def delete_bundles_allowed_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed bundle allowed R'{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteBundlesAllowedRole", role_id)

    async def delete_bundles_role(self, role_id: int) -> bool:
        await self._log_sql_event(f"Removed bundle R'{role_id}'", "INFO")
        return await self._execute_write_operation("ExoDeleteBundlesRole", role_id)
     
    async def is_bundle_allowed_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsBundleAllowedRole", role_id))[0][0])
    
    async def is_bundle_role(self, role_id: int) -> bool:
        return bool((await self._execute_read_operation("ExoIsBundleRole", role_id))[0][0])
   
    async def count_bundles(self, guild_id: int) -> int:
        return int((await self._execute_read_operation("ExoCountBundles", guild_id))[0][0])
    
    async def count_bundles_choices(self, allowed_roles: list[BundleRole]) -> int:
        choices = await self.get_bundles_choices(allowed_roles)
        return len(choices)

def setup(bot):
    bot.add_cog(Data(bot))