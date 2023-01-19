from discord import Message, TextChannel
from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands
from discord.member import Member
from discord.role import Role
from enum import Enum
from discord.file import File
from PIL import Image, ImageDraw, ImageFilter
import requests
import traceback

class Permission(Enum):
    manageroles = 0
    sendmessage = 1
    embedlinks = 2

class Embeds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def generate_embed(self, title: str, content: str, color: int = 0xCC0000) -> Embed :
        embed: Embed
        try:
            embed = Embed(title=title, description=content, colour=color)

        except Exception as e:
            embed = await self.generate_embed_unexpected_error()
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'embeds - generate_embed', traceback.format_exc(), title, content, color)

        return embed

    async def generate_embed_args_error(self, command: str, argcount: int) -> Embed :
        return await self.generate_embed("Missing arguments", f"Command '{command}' requires a minimum of {argcount} extra arguments.")

    async def generate_embed_int_parsing_error(self, string: str) -> Embed:
        return await self.generate_embed("Parsing error", f"Exophose cannot parse '{string}' as it is not a valid number.")

    async def generate_embed_color_parsing_error(self, rolecolor: str) -> Embed :
        return await self.generate_embed("Parsing error", f"Exophose cannot parse color '{rolecolor}' as it is either not a hexadecimal number or not between #000000 and #FFFFFF.")

    async def generate_embed_unexpected_error(self) -> Embed :
        return await self.generate_embed("Unexpected Error", f"Exophose encountered an unexpected error.")

    async def generate_embed_unexpected_sql_error(self) -> Embed :
        return await self.generate_embed("Unexpected SQL Error", f"Exophose encountered an unexpected error with the SQL database. Impossible to complete this action at the moment. This may highly be due to the SQL server being under maintenance. I have no control over this.")

    async def generate_embed_forbidden_error(self) -> Embed :
        return await self.generate_embed("403 Forbidden", f"Exophose encountered a forbidden error while trying to edit a role. Make sure it was not moved above the bot's role.")

    async def generate_embed_allowed_roles(self, guildid: str) -> Embed :
        embed: Embed
        try:
            data = self.bot.get_cog("Data")
            if data is not None:
                guildallowedroles = await data.get_allowed_roles_by_guild(guildid)

                if len(guildallowedroles) > 0 :
                    embed = Embed(title="Allowed Roles", description="Here is a list of the allowed roles in your guild.", colour=0xFFFFFF)

                    for row in guildallowedroles:
                        numroles: int = row[4]
                        badgeallowed: bool = row[8]
                        newline = "\n"
                        embed.add_field(name=f"\u200b", value=f"{f'<@&{row[1]}>' if row[1] != row[2] else '**everyone**'}  |  Can create **{numroles}** role{'s' if numroles > 1 else ''}  |  **Can{'' if badgeallowed else 'not'}** add custom badges{newline}Allowed by <@{row[3]}> on **<t:{int(row[5].timestamp())}>**{'' if row[6] is None else f'{newline}Last update by <@{row[6]}> on **<t:{int(row[7].timestamp())}>**'}", inline=False)
                else :
                    embed = Embed(title="Allowed Roles", description="Your guild has no allowed roles.", colour=0xFFFFFF)
            
        except Exception as e:
            embed = await self.generate_embed_unexpected_error()
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'embeds - generate_embed_allowed_roles', traceback.format_exc())
        
        return embed

    async def generate_embed_missing_permissions(self, *permissions: Permission) -> Embed :
        message = "Exophose requires "

        for permission in permissions:
            if permission == Permission.manageroles:
                message += "`Manage_Roles` "
            elif permission == Permission.sendmessage:
                message += "`Send_message` "
            else:
                message += "`Embed_Links` "

        message += "permission(s) to run that command. Make sure they are on the role itself."

        return await self.generate_embed("Permission Error", message)

    async def generate_embed_created_roles(self, member: Member) -> Embed :
        embed: Embed
        try:
            data = self.bot.get_cog("Data")
            if data is not None:
                usercreatedroles = await data.get_created_roles_by_guild_by_user(member.guild.id, member.id)

                if len(usercreatedroles) > 0 :
                    embed = Embed(title="Created Roles", description=f"Here is a list of the created roles for {member.mention}.", colour=0xFFFFFF)

                    index: int = 0
                    for row in usercreatedroles:
                        role: Role = member.guild.get_role((int)(row[1]))
                        newline = "\n"
                        embed.add_field(name=f"\u200b", value=f"Index: `{index}`  |  <@&{row[1]}>  |  Color: `#{hex(role.colour.value)[2:]}`{'' if role.icon is None or role.icon.url is None else f'  |  [View badge]({role.icon.url})'}{newline}Created on **<t:{int(row[4].timestamp())}>**", inline=False)
                        index += 1
                else :
                    embed = Embed(title="Created Roles", description=f"{member.mention} has not created any roles.", colour=0xFFFFFF)
            
        except Exception as e:
            embed = await self.generate_embed_unexpected_error()
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'embeds - generate_embed_created_roles', traceback.format_exc())

        return embed

    async def generate_embed_preview_color(self, member: Member, color: str) -> Embed:

        embed: Embed = None
        file: str = ""
        hexcolor = None
            
        try:
            utilities = self.bot.get_cog("Utilities")
            if utilities is not None:
                if color is not None:
                    hexcolor = await utilities.parse_color(color)
                if hexcolor is not None:
                    hexstrcolor : str = "{0:#0{1}x}".format(hexcolor, 8)[2:]
                    embed = await self.generate_embed(f"Color preview for #{hexstrcolor}", "If you want to preview other colors, you can use an [online color picker](https://g.co/kgs/Ye7sc5). Make sure to use the hexadecimal value.", hexcolor)
                    

                    img = Image.new('RGB', (300, 300), tuple(int(hexstrcolor[i:i+2], 16) for i in (0, 2, 4)))

                    avatarpath: str = ""
                    if member.avatar is not None:
                        avatarpath = member.avatar.url
                        if member.guild_avatar is not None:
                            avatarpath = member.guild_avatar.url
                        
                        avatarpath256 = avatarpath.replace("size=1024", "size=256")
                        pfp = Image.open(requests.get(avatarpath256, stream=True).raw)
                        mask = Image.new("L", pfp.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0, 255, 255), fill=255)
                        img.paste(pfp, (22, 22), mask.filter(ImageFilter.GaussianBlur(3)))
                    
                    file = f"./temp/{member.id}_{hex(hexcolor)[2:]}.jpg"
                    img.save(file, quality=100)

                    imagechannel: TextChannel = self.bot.get_channel("YOUR TEMPORARY IMAGE CREATION CHANNEL")
                    message: Message = await imagechannel.send(file=File(file))

                    embed.set_thumbnail(url=message.attachments[0].url)

                    await message.delete()

                else:
                    embed = await self.generate_embed("Color preview", "To preview colors, you can use an [online color picker](https://g.co/kgs/Ye7sc5). Make sure to use the hexadecimal value.", 0xFFFFFF)
                
        except Exception as e:
            embed = await self.generate_embed_unexpected_error()
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'embeds - generate_embed_preview_color', traceback.format_exc())
        
        return embed

    async def generate_embed_missing_index(self) -> Embed:
        return await self.generate_embed("Missing index", f"No index was provided. If you wish to remove all of your custom roles at once, use /remove `index:`all.")

    async def generate_embed_not_admin_allowed(self) -> Embed :
        return await self.generate_embed("User not allowed", "You are not allowed to use this command as you do not have administrator permissions.")

    async def generate_embed_not_user_allowed(self) -> Embed :
        return await self.generate_embed("User not allowed", "You are not allowed to create custom roles for yourself as you have none of the allowed roles.")

    async def generate_embed_not_badge_allowed(self) -> Embed :
        return await self.generate_embed("User not allowed", "You are not allowed to set custom badges with your currently allowed role(s).")

    async def generate_embed_success_modification(self, action: str) -> Embed:
        return await self.generate_embed(f"Role {action} success", f"Exophose successfully {action}{'d' if action.endswith('e') else 'ed'} your role.", 0x00CC00)

    async def generate_embed_fail_index_modification(self, action: str) -> Embed: 
        return await self.generate_embed(f"Role {action} error", f"You must specify a valid index for the role you want to {action}.")

    async def generate_embed_fail_missing_modification(self, action: str) -> Embed: 
        return await self.generate_embed(f"Role {action} error", f"Exophose cannot {action} your custom role as you do not have one.")

    async def generate_embed_not_link_allowed(self) -> Embed: 
        return await self.generate_embed("Invalid link", "The link you have provided is invalid. Make sure it's a `cdn.discordapp.com` or `media.discordapp.net` link containing an image of extension `.jpg`, `.jpeg` or `.png`.")

    async def generate_embed_link_error(self) -> Embed: 
        return await self.generate_embed("No access", "The link you have provided was valid but exophose cannot access it. Make sure it's not an image posted through Direct Messages, except for Exophose's.")

    async def generate_cog_restarted(self, cog: str) -> Embed :
        return await self.generate_embed("Cog Restarted", f"`{cog}` cog was successfully restarted.")

    async def generate_cog_restart_error(self, cog: str) -> Embed :
        return await self.generate_embed("Cog Restart Failed", f"`{cog}` cog could not be restarted.")

    async def generate_no_cog_found(self, cog: str) -> Embed :
        return await self.generate_embed("Cog Not Found", f"`{cog}` cog was not found. Double-check availability.")


def setup(bot):
    bot.add_cog(Embeds(bot))