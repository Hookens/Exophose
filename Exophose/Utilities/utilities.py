from discord.bot import Bot
from discord.ext import commands
from discord.guild import Guild
from discord.member import Member
from discord.role import Role
import traceback
import requests

class Utilities(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def parsable_int(self, string: str) -> bool:
        try:
            integer: int = int(string)
            return True
        except Exception:
            return False

    def parsable_color(self, color: str) -> bool:
        try:
            intcolor: int = int(color, 16)
            return True
        except Exception as e:
            return False

    async def parse_color (self, color: str):
        """Turns a string into a hexacedimal int representing a color.\n
        Returns: The int value, or an empty string if the original string is invalid."""

        intcolor = None
        hexcolor = color.replace('#', '')

        try:
            if self.parsable_color(hexcolor):
                intcolor = int(hexcolor, 16)
                if intcolor > 0xFFFFFF or intcolor < 0 :
                    intcolor = None
                elif intcolor == 0:
                    intcolor = 0x010101
            return intcolor
        
        except Exception as e:
            #await log_error(e, "Exophose", 'utilities - parse_color', traceback.format_exc())
            return None

    async def get_member_in_guild(self, guild: Guild, userid = None) -> Member:
        try :
            if self.parsable_int(userid):
                return guild.get_member(int(userid))
            return None
        except Exception as e :
            #await log_error(e, "Exophose", 'utilities - get_member_in_guild', traceback.format_exc())
            return None

    async def reposition (self, role: Role):
        try:
            data = self.bot.get_cog("Data")
            if data is not None:
                botrole = role.guild.get_role(await data.get_exophose_role_by_guild(str(role.guild.id)))

                if botrole :
                    if botrole.permissions.manage_roles:
                        i = 1
                        while botrole.position - i > 1:
                            try:
                                await role.edit(position=(botrole.position - i))
                                break
                            except Exception as e:
                                logging = self.bot.get_cog("Logging")
                                if logging is not None:
                                    await logging.log_error(e,'utilities - reposition', traceback.format_exc(), botrole.position, role.position, i, botrole.position - i)
                                i += 1

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'utilities - reposition', traceback.format_exc(), botrole.position, role.position)

    async def fetch_image(self, link: str) -> bytes:
        try:
            image: bytes = requests.get(link).content
            return image
        except Exception as e:
            return None

def setup(bot):
    bot.add_cog(Utilities(bot))