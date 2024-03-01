import os
from discord import Message
from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands
from discord.member import Member
from discord.role import Role
from discord.file import File
from PIL import Image, ImageDraw, ImageFilter
import requests

from Debug.debughelpers import try_func_async
from Utilities.datahelpers import AllowedRole, CreatedRole

WHITE = 0xFFFFFF
GREEN = 0x00CC00
RED = 0xCC0000

TEMP_IMG_CHANNEL = 1027991803540025454

class Embeds(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def _get_cogs(self, include_data: bool = False, include_utilities: bool = False) -> tuple:
        data = self.bot.get_cog("Data") if include_data else None
        utilities = self.bot.get_cog("Utilities") if include_utilities else None
        
        if ((data is None and include_data) or 
            (utilities is None and include_utilities)):
            raise(ValueError("One or more cogs are missing.", data, utilities))
        
        return tuple(filter(None, (data, utilities)))

    def generate_embed(self, title: str, description: str, color: int = RED, image: str = None, footer: str = None, **kwargs) -> Embed:
        embed = Embed(title=title, description=description, colour=color)
        if image is not None:
            embed.set_thumbnail(url=image)
        if footer is not None:
            embed.set_footer(text=footer)
            
        for key, value in kwargs.items():
            embed.add_field(name=key, value=value, inline=False)

        return embed

    def blacklisted_word(self) -> Embed:
        return self.generate_embed("Blacklisted Word", "The role must not contain profane or offensive words.")

    def creation_success(self) -> Embed:
        return self.generate_embed("Role creation success", f"Exophose successfully created your new role.", GREEN)

    def maximum_roles(self) -> Embed:
        return self.generate_embed("Maximum Roles", "You have reached the maximum number of roles for your allowed role.")

    #Admin
    def allowed_role_added(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose allowed {role.mention} to use role management commands.", color=GREEN)

    def allowed_role_updated(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose updated the permissions for {role.mention}.", GREEN)

    def allowed_role_removed(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose disallowed {role.mention} from using role management commands.", GREEN)

    def allowed_role_error(self, role: Role) -> Embed:
        return self.generate_embed("Unable to allow role", f"Exophose cannot allow {role.mention}. You have reached the maximum of 20 allowed roles.")

    def allowed_role_missing(self, role: Role) -> Embed:
        return self.generate_embed("Unable to disallow role", f"Exophose cannot disallow {role.mention} as it is already disallowed.")
    
    @try_func_async(embed=True)
    async def allowed_roles(self, guild_id: int) -> Embed:
        (data,) = self._get_cogs(include_data=True)

        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

        if not any(allowed_roles):
            return self.generate_embed("Allowed Roles", "Your server has no allowed roles.", WHITE)

        embed = self.generate_embed("Allowed Roles", "Here is a list of the allowed roles in your server.", WHITE)

        for allowed_role in allowed_roles:
            ping = "**everyone**" if allowed_role.is_everyone else f"<@&{allowed_role.id}>"
            role_plural = "s" if allowed_role.max_roles > 1 else ""
            max_roles = f"Can create **{allowed_role.max_roles}** role{role_plural}"
            not_badges = "" if allowed_role.allow_badges else "not"
            allow_badges = f"**Can{not_badges}** add custom badges"
            allowed_by = f"Allowed by <@{allowed_role.user_id}> on **<t:{int(allowed_role.created_date.timestamp())}>**"
            updated_by = f"\nLast update by <@{allowed_role.updated_user_id}> on **<t:{int(allowed_role.updated_date.timestamp())}>**" if allowed_role.updated_user_id is not None else ""
            field = f"{ping} | {max_roles} | {allow_badges}\n{allowed_by}{updated_by}"

            embed.add_field(name="\u200b", value=field, inline=False)

        return embed

    #User
    @try_func_async(embed=True)
    async def created_roles(self, member: Member) -> Embed:
        (data,) = self._get_cogs(include_data=True)
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.guild.id, member.id)

        if not any(created_roles):
            return self.generate_embed("Created Roles", f"{member.mention} has not created any roles.", WHITE)
        
        embed = self.generate_embed("Created Roles", f"Here is a list of the created roles for {member.mention}.", WHITE)

        i: int = 0
        for created_role in created_roles:
            role: Role = member.guild.get_role(created_role.id)
            index = f"Index: `{i}`"
            ping = f"<@&{role.id}>"
            hexstrcolor = "{0:#0{1}x}".format(role.colour.value, 8)[2:]
            color = f"Color: `#{hexstrcolor}`"
            badge = f" | [View badge]({role.icon.url})" if role.icon is not None else ""
            created_date = f"Created on **<t:{int(created_role.created_date.timestamp())}>**"
            field = f"{index} | {ping} | {color}{badge}\n{created_date}"

            embed.add_field(name=f"\u200b", value=field, inline=False)
            i += 1

        return embed

    @try_func_async(embed=True)
    async def preview_color(self, member: Member, color: str) -> Embed:
        (utilities,) = self._get_cogs(include_utilities=True)
            
        hexcolor = await utilities.parse_color(color)

        if hexcolor is None:
            return self.generate_embed("Color preview", "To preview colors, you can use an [online color picker](https://www.google.com/search?q=colorpicker). Make sure to use the hexadecimal value.", WHITE)
        
        hexstrcolor : str = "{0:#0{1}x}".format(hexcolor, 8)[2:]
        embed = self.generate_embed(f"Color preview for #{hexstrcolor}", "If you want to preview other colors, you can use an [online color picker](https://www.google.com/search?q=colorpicker). Make sure to use the hexadecimal value.", hexcolor)
        
        img = Image.new('RGB', (300, 300), tuple(int(hexstrcolor[i:i+2], 16) for i in (0, 2, 4)))

        if (avatar := member.guild_avatar or member.avatar) is not None:
            avatarpath256 = avatar.url.replace("size=1024", "size=256")
            pfp = Image.open(requests.get(avatarpath256, stream=True).raw)
            mask = Image.new("L", pfp.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 255, 255), fill=255)
            img.paste(pfp, (22, 22), mask.filter(ImageFilter.GaussianBlur(3)))
        
        file = f"./temp/{member.id}_{hex(hexcolor)[2:]}.jpg"
        img.save(file, quality=100)

        message: Message = await self.bot.get_channel(TEMP_IMG_CHANNEL).send(file=File(file))

        embed.set_thumbnail(url=message.attachments[0].url)

        await message.delete()
        os.remove(file)

    def success_modification(self, action: str) -> Embed:
        return self.generate_embed(f"Role {action} success", f"Exophose successfully {action}{'d' if action.endswith('e') else 'ed'} your role.", GREEN)

    def missing_modification_index(self, action: str) -> Embed: 
        return self.generate_embed(f"Role {action} error", f"You must specify a valid index for the role you want to {action}.")

    def missing_modification_role(self, action: str) -> Embed: 
        return self.generate_embed(f"Role {action} error", f"Exophose cannot {action} your custom role as you do not have one.")

    #Errors
    def color_parsing_error(self) -> Embed:
        return self.generate_embed("Parsing error", f"Exophose cannot parse the given color as it is either not a hexadecimal number or not between #000000 and #FFFFFF.")

    def unexpected_error(self) -> Embed:
        return self.generate_embed("Unexpected Error", f"Exophose encountered an unexpected error.")

    def unexpected_sql_error(self) -> Embed:
        return self.generate_embed("Unexpected SQL Error", f"Exophose encountered an unexpected error with the SQL database. Impossible to complete this action at the moment. This may highly be due to the SQL server being under maintenance. I have no control over this.")

    def forbidden_error(self) -> Embed:
        return self.generate_embed("403 Forbidden", f"Exophose encountered a forbidden error while trying to edit a role. Make sure it was not moved above the bot's role.")

    #Verification
    def not_user_allowed(self) -> Embed:
        return self.generate_embed("User not allowed", "You are not allowed to create custom roles for yourself as you have none of the allowed roles.")

    def not_badge_allowed(self) -> Embed:
        return self.generate_embed("User not allowed", "You are not allowed to set custom badges with your currently allowed role(s).")

    def not_file_allowed(self) -> Embed: 
        return self.generate_embed("Invalid File", "The file you have provided is invalid. Make sure it's an image file type supported by discord (.png, .jpg, .webp).")

    def not_permission_allowed(self) -> Embed:
        return self.generate_embed("Permission Error", "Exophose is missing `Manage_Roles` permission.")

    def not_feature_allowed(self) -> Embed:
        return self.generate_embed("Missing feature", "Your server does not have role bages unlocked as they are a level 2 boost feature.")

    #Debug
    def cog_restarted(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restarted", f"`{cog}` cog was successfully restarted.", color=GREEN)

    def cog_restart_error(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restart Failed", f"`{cog}` cog could not be restarted.")


def setup(bot):
    bot.add_cog(Embeds(bot))