import asyncio
from datetime import datetime
from discord.bot import Bot
from discord.ext import commands
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

EXODB: MySQLConnection = None
LASTCONNECT: datetime = datetime.now().timestamp() - 1000

HST = 'YOUR DATABASE HOST'
USR = 'YOUR DATABASE USER'
PWD = 'YOUR DATABASE PASSWORD'

class Data(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
    async def reconnect(self) -> bool:
        global EXODB
        global LASTCONNECT
        try:
            if EXODB is not None:
                EXODB.close()
            EXODB = mysql.connector.connect(host=HST, user=USR, password=PWD, database=USR)
            LASTCONNECT = datetime.now().timestamp()
            return True
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_sql_error(error=e, function='SQL - reconnect')
            return False

    async def add_exophose_role(self, roleid: str, guildid: str) -> bool:
        global EXODB
        global LASTCONNECT
        msg: str = f"Exophose was added to guild '{guildid}'"
        if roleid == '0':
            msg += " without a role."
        else:
            msg += f" with role '{roleid}'."
        logging = self.bot.get_cog("Logging")
        if logging is not None:
            await logging.log_event(msg, "INFO")

        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                insertsql = "INSERT INTO ExophoseRole (roleid, guildid) VALUES (%s, %s)"
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.execute(insertsql, (roleid,guildid))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - add_exophose_role', roleid=roleid, guildid=guildid)
                await asyncio.sleep(4)
            break
        return False

    async def add_allowed_role(self, roleid: str, guildid: str, userid: str, maxroles, allowbadges) -> bool:
        global EXODB
        global LASTCONNECT
        logging = self.bot.get_cog("Logging")
        if logging is not None:
            await logging.log_event(f"User '{userid}' allowed role '{roleid}' in guild '{guildid}' to create '{maxroles}' roles {'with' if allowbadges else 'without'} badges.", "INFO")

        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                insertsql = "INSERT INTO AllowedRoles (roleid, guildid, userid, maxroles, allowbadges) VALUES (%s, %s, %s, %s, %s)"
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.execute(insertsql, (roleid, guildid, userid, maxroles, allowbadges))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - add_allowed_role', roleid=roleid, guildid=guildid, userid=userid)
                await asyncio.sleep(4)
            break
        return False
        
    async def update_allowed_role(self, guildid: str, roleid: str, userid: str, maxroles, allowbadges) -> bool:
        global EXODB
        global LASTCONNECT
        logging = self.bot.get_cog("Logging")
        if logging is not None:
            escaped = "\'"
            await logging.log_event(f"User '{userid}' updated allowed role '{roleid}' to now create {f'{escaped}{maxroles}{escaped} ' if maxroles > 0 else ''}roles {'with' if allowbadges else 'without'} badges in guild {guildid}.", "INFO")

        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("UpdateAllowedRole", (guildid, roleid, userid, maxroles, allowbadges))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - update_allowed_role', guildid=guildid, roleid=roleid, userid=userid)
                await asyncio.sleep(4)
            break
        return False

    async def add_created_role(self, roleid: str, guildid: str, userid: str) -> bool:
        global EXODB
        global LASTCONNECT
        logging = self.bot.get_cog("Logging")
        if logging is not None:
            await logging.log_event(f"User '{userid}' created role '{roleid}' in guild '{guildid}'.", "INFO")

        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                insertsql = "INSERT INTO CreatedRoles (roleid, guildid, userid) VALUES (%s, %s, %s)" 
                DBCURSOR: CursorBase =EXODB.cursor()
                DBCURSOR.execute(insertsql, (roleid,guildid,userid))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - add_created_role', roleid=roleid, guildid=guildid, userid=userid)
                await asyncio.sleep(4)
            break
        return False

    async def get_exophose_role_by_guild(self, guildid: str) -> int:
        global EXODB
        global LASTCONNECT

        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return 0

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("GetExophoseRoleByGuild", (guildid,))
                for result in DBCURSOR.stored_results():
                    guildexophoserole=result.fetchall()
                DBCURSOR.close()
                
                if guildexophoserole != []:
                    return int(guildexophoserole[0][0])
                else: 
                    return 0
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - get_exophose_role_by_guild', guildid=guildid)
                await asyncio.sleep(4)
            break
        return 0

    async def get_allowed_roles_by_guild(self, guildid: str):
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return None

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("GetAllowedRolesByGuild", (guildid,))
                for result in DBCURSOR.stored_results():
                    guildallowedroles=result.fetchall()
                DBCURSOR.close()
                
                return guildallowedroles
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - get_allowed_roles_by_guild', guildid=guildid)
                await asyncio.sleep(4)
            break
        return None

    async def get_created_roles_by_guild_by_user(self, guildid: str, userid: str):
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("GetCreatedRolesByGuildByUser", (guildid,userid))
                for result in DBCURSOR.stored_results():
                    usercreatedroles=result.fetchall()
                DBCURSOR.close()
                
                return usercreatedroles
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - get_created_roles_by_guild_by_user', guildid=guildid, userid=userid)
                await asyncio.sleep(4)
            break
        return None

    async def delete_exophose_role_by_guild(self, guildid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteExophoseRoleByGuild", (guildid,))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_exophose_role_by_guild', guildid=guildid)
                await asyncio.sleep(4)
            break
        return False

    async def delete_allowed_role_by_role(self, roleid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteAllowedRoleByRole", (roleid,))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_allowed_role_by_role', roleid=roleid)
                await asyncio.sleep(4)
            break
        return False

    async def delete_allowed_roles_by_guild(self, guildid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteAllowedRolesByGuild", (guildid,))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_allowed_roles_by_guild', guildid=guildid)
                await asyncio.sleep(4)
            break
        return False

    async def delete_created_role_by_role(self, roleid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteCreatedRoleByRole", (roleid,))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_created_role_by_role', roleid=roleid)
                await asyncio.sleep(4)
            break
        return False

    async def delete_created_roles_by_guild(self, guildid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteCreatedRolesByGuild", (guildid,))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_created_roles_by_guild', guildid=guildid)
                await asyncio.sleep(4)
            break
        return False

    async def delete_created_roles_by_guild_by_user(self, guildid: str, userid: str) -> bool:
        global EXODB
        global LASTCONNECT
        if datetime.now().timestamp() - LASTCONNECT > 300:
            if not await self.reconnect():
                return False

        while True:
            try:
                DBCURSOR: CursorBase = EXODB.cursor()
                DBCURSOR.callproc("DeleteCreatedRolesByGuildByUser", (guildid,userid))
                DBCURSOR.close()
                EXODB.commit()
                
                return True
            except Exception as e:
                if datetime.now().timestamp() - LASTCONNECT > 10:
                    if await self.reconnect():
                        continue
                logging = self.bot.get_cog("Logging")
                if logging is not None:
                    await logging.log_sql_error(error=e, function='SQL - delete_created_roles_by_guild_by_user', guildid=guildid)
                await asyncio.sleep(4)
            break
        return False
    


def setup(bot):
    bot.add_cog(Data(bot))