# Copyright (C) 2025 Hookens
# See the LICENSE file in the project root for details.

import os
from discord import Message
from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands
from discord.member import Member
from discord.role import Role
from discord.file import File
#from PIL import Image, ImageDraw, ImageFilter
import requests

from Debug.debughelpers import try_func_async
from Utilities.constants import EmbedDefaults
from Utilities.datahelpers import Bundle, BundleRole, AllowedRole, CreatedRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.utilities import Utilities

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

    def generate_embed(self, title: str, description: str, color: int = EmbedDefaults.RED, image: str = None, footer: str = None, **kwargs) -> Embed:
        embed = Embed(title=title, description=description, colour=color)
        if image is not None:
            embed.set_thumbnail(url=image)
        if footer is not None:
            embed.set_footer(text=footer)
            
        for key, value in kwargs.items():
            embed.add_field(name=key, value=value, inline=False)

        return embed

    def blacklisted_word(self) -> Embed:
        return self.generate_embed("Blacklisted Word", "The name must not contain profane or offensive words.")

    def creation_success(self) -> Embed:
        return self.generate_embed("Role creation success", f"Exophose successfully created your new role.", EmbedDefaults.GREEN)

    def maximum_roles(self) -> Embed:
        return self.generate_embed("Maximum Roles", "You have reached the maximum number of roles for your allowed role.")

    def maximum_bundles(self) -> Embed:
        return self.generate_embed("Maximum Bundles", "Maximum number of bundles reached for your server.")


    #Admin
    def allowed_role_added(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose allowed {role.mention} to use role management commands.", color=EmbedDefaults.GREEN)

    def allowed_role_updated(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose updated the permissions for {role.mention}.", EmbedDefaults.GREEN)

    def allowed_role_removed(self, role: Role) -> Embed:
        return self.generate_embed("Configuration changed", f"Exophose disallowed {role.mention} from using role management commands.", EmbedDefaults.GREEN)

    def allowed_role_error(self, role: Role) -> Embed:
        return self.generate_embed("Unable to allow role", f"Exophose cannot allow {role.mention}. You have reached the maximum of 20 allowed roles.")

    def allowed_role_missing(self, role: Role) -> Embed:
        return self.generate_embed("Unable to disallow role", f"Exophose cannot disallow {role.mention} as it is already disallowed.")
    
    @try_func_async(embed=True)
    async def allowed_roles(self, guild_id: int) -> Embed:
        data: Data
        (data,) = self._get_cogs(include_data=True)

        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(guild_id)

        if not any(allowed_roles):
            return self.generate_embed("Allowed Roles", "Your server has no allowed roles.", EmbedDefaults.WHITE)

        embed = self.generate_embed("Allowed Roles", "Here is a list of the allowed roles in your server.", EmbedDefaults.WHITE)

        for allowed_role in allowed_roles:
            ping = "**everyone**" if allowed_role.is_everyone else f"<@&{allowed_role.id}>"
            role_plural = "s" if allowed_role.max_roles > 1 else ""
            max_roles = f"**{allowed_role.max_roles}** role{role_plural}"
            not_badges = ":white_check_mark:" if allowed_role.allow_badges else ":no_entry_sign:"
            not_gradients = ":white_check_mark:" if allowed_role.allow_gradients else ":no_entry_sign:"
            allow_badges = f"{not_badges} custom badges"
            allow_gradients = f"{not_gradients} enhanced role styles"
            allowed_by = f"Allowed by <@{allowed_role.user_id}> on **<t:{int(allowed_role.created_date.timestamp())}>**"
            updated_by = f"\nLast update by <@{allowed_role.updated_user_id}> on **<t:{int(allowed_role.updated_date.timestamp())}>**" if allowed_role.updated_user_id is not None else ""
            field = f"{ping} | {max_roles} | {allow_gradients} | {allow_badges}\n{allowed_by}{updated_by}"

            embed.add_field(name="\u200b", value=field, inline=False)

        return embed


    #User
    @try_func_async(embed=True)
    async def created_roles(self, member: Member) -> Embed:
        data: Data
        (data,) = self._get_cogs(include_data=True)
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.guild.id, member.id)

        if not any(created_roles):
            return self.generate_embed("Created Roles", f"{member.mention} has not created any roles.", EmbedDefaults.WHITE)
        
        embed = self.generate_embed("Created Roles", f"Here is a list of the created roles for {member.mention}.", EmbedDefaults.WHITE)

        i: int = 0
        for created_role in created_roles:
            role: Role = member.guild.get_role(created_role.id)
            index = f"Index: `{i}`"
            ping = f"<@&{role.id}>"
            hexstrcolor = "{0:#0{1}x}".format(role.colour.value, 8)[2:]
            hexstrseccolor = "{0:#0{1}x}".format(role.colors.secondary.value, 8)[2:] if role.colors.secondary else None
            color = "`Holographic`" if (role.colors.tertiary and role.colors.is_holographic) else f"`#{hexstrcolor}` -> `{hexstrseccolor}`" if hexstrseccolor else f"`#{hexstrcolor}`"
            badge = f" | [View badge]({role.icon.url})" if role.icon is not None else ""
            created_date = f"Created on **<t:{int(created_role.created_date.timestamp())}>**"
            field = f"{index} | {ping} | {color}{badge}\n{created_date}"

            embed.add_field(name=f"\u200b", value=field, inline=False)
            i += 1

        return embed

    @try_func_async(embed=True)
    async def preview_color(self, member: Member, color: str) -> Embed:
        utilities: Utilities
        (utilities,) = self._get_cogs(include_utilities=True)
            
        hexcolor = await utilities.parse_color(color) if color else None

        if hexcolor is None:
            return self.generate_embed("Color preview", "To preview colors, you can use an [online color picker](https://www.google.com/search?q=colorpicker). Make sure to use the hexadecimal value.", EmbedDefaults.WHITE)
        
        hexstrcolor : str = "{0:#0{1}x}".format(hexcolor, 8)[2:]
        embed = self.generate_embed(f"Color preview for #{hexstrcolor}", "If you want to preview other colors, you can use an [online color picker](https://www.google.com/search?q=colorpicker). Make sure to use the hexadecimal value.", hexcolor)
        
        #img = Image.new('RGB', (300, 300), tuple(int(hexstrcolor[i:i+2], 16) for i in (0, 2, 4)))

        #if (avatar := member.guild_avatar or member.avatar) is not None:
        #    avatarpath256 = avatar.url.replace("size=1024", "size=256")
        #    pfp = Image.open(requests.get(avatarpath256, stream=True).raw)
        #    mask = Image.new("L", pfp.size, 0)
        #    draw = ImageDraw.Draw(mask)
        #    draw.ellipse((0, 0, 255, 255), fill=255)
        #    img.paste(pfp, (22, 22), mask.filter(ImageFilter.GaussianBlur(3)))
        #
        #file = f"./temp/{member.id}_{hex(hexcolor)[2:]}.jpg"
        #img.save(file, quality=100)

        #message: Message = await self.bot.get_channel(EmbedDefaults.TEMP_IMG_CHANNEL).send(file=File(file))

        #embed.set_thumbnail(url=message.attachments[0].url)

        #os.remove(file)

        return embed

    def success_modification(self, action: str) -> Embed:
        return self.generate_embed(f"Role {action} success", f"Exophose successfully {action}{'d' if action.endswith('e') else 'ed'} your role.", EmbedDefaults.GREEN)

    def missing_modification_index(self, action: str) -> Embed: 
        return self.generate_embed(f"Role {action} error", f"You must specify a valid index for the role you want to {action}.")

    def missing_modification_role(self, action: str) -> Embed: 
        return self.generate_embed(f"Role {action} error", f"Exophose cannot {action} your custom role as you do not have one.")


    #Errors
    def color_parsing_error(self) -> Embed:
        return self.generate_embed("Parsing error", f"Exophose cannot parse the given color as it is not a hexadecimal number.")

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

    def not_role_allowed(self, role: Role) -> Embed:
        return self.generate_embed("Permission Error", f"Exophose is unable to grant {role.mention}.")

    def not_edit_allowed(self, role: Role, action: str) -> Embed:
        return self.generate_embed("Permission Error", f"Exophose cannot {action} {role.mention} because it is too high in the hierarchy.")

    def not_feature_allowed(self) -> Embed:
        return self.generate_embed("Missing feature", "Your server does not have role bages unlocked as they are a level 2 boost feature.")


    #Bundle
    def not_bundle_allowed(self) -> Embed:
        return self.generate_embed("User not allowed", "You are not allowed to use any of the bundles.")

    def no_bundle_roles(self) -> Embed:
        return self.generate_embed("User not allowed", "You are not allowed to use any of the bundles.")

    def bundle_created(self, name: str) -> Embed:
        return self.generate_embed("Bundle created", f"Exophose created a new bundle named {name}.", color=EmbedDefaults.GREEN)
    
    def bundle_deleted(self) -> Embed:
        return self.generate_embed("Bundle deleted", f"Exophose deleted the bundle.", color=EmbedDefaults.GREEN)
    
    def bundle_role_selected(self, role: Role) -> Embed:
        return self.generate_embed("Role selected", f"Exophose granted you {role.mention}.", color=EmbedDefaults.GREEN)
    
    def bundle_missing_index(self, action: str) -> Embed:
        return self.generate_embed(f"Bundle {action} invalid", f"You must specify a valid index for the bundle you want to {action}.")
    
    def bundle_missing_choice_index(self) -> Embed:
        return self.generate_embed(f"Role selection invalid", f"You must specify a valid index for the role you want to choose.")
    
    def bundle_selection_invalid(self) -> Embed:
        return self.generate_embed(f"Bundle selection invalid", f"You must enter the matching index and name of the bundle to confirm its deletion.")
    

    def bundle_allowed_role_added(self, role: Role) -> Embed:
        return self.generate_embed("Bundle allowed role added", f"Exophose allowed {role.mention} in the bundle.", color=EmbedDefaults.GREEN)
    
    def bundle_allowed_role_removed(self, role: Role) -> Embed:
        return self.generate_embed("Bundle allowed role removed", f"Exophose disallowed {role.mention} from the bundle.", color=EmbedDefaults.GREEN)
    
    def bundle_allowed_role_present(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role allow impossible", f"Exophose cannot allow {role.mention} in the bundle as it is already allowed.")
    
    def bundle_allowed_role_missing(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role disallow impossible", f"Exophose cannot disallow {role.mention} from the bundle as it is already disallowed.")
    
    def bundle_allowed_role_error(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role allow impossible", f"Exophose cannot allow {role.mention} in the bundle. You have reached the maximum of 10 roles.")
    

    def bundle_role_added(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role added", f"Exophose added {role.mention} to the bundle.", color=EmbedDefaults.GREEN)
    
    def bundle_role_removed(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role removed", f"Exophose removed {role.mention} from the bundle.", color=EmbedDefaults.GREEN)
    
    def bundle_role_present(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role add impossible", f"Exophose cannot add {role.mention} to the bundle as it is already present.")
    
    def bundle_role_missing(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role remove impossible", f"Exophose cannot remove {role.mention} from the bundle as it is already not present.")
    
    def bundle_role_error(self, role: Role) -> Embed:
        return self.generate_embed("Bundle role add impossible", f"Exophose cannot add {role.mention} to the bundle. You have reached the maximum of 10 roles.")

    @try_func_async(embed=True)
    async def bundle_list(self, guild_id) -> Embed:
        data: 'Data'
        (data,) = self._get_cogs(include_data=True)

        bundles: list[Bundle] = await data.get_bundles(guild_id)

        if not any(bundles):
            return self.generate_embed("Created Bundles", f"There are no created bundles in your server.", EmbedDefaults.WHITE)
        
        embed = self.generate_embed("Created Bundles", f"Here is a list of the bundles in your server.", EmbedDefaults.WHITE)
        
        i: int = 0
        for bundle in bundles:
            bundle_allowed_roles: list[BundleRole] = await data.get_bundle_allowed_roles(bundle.id)
            bundle_roles: list[BundleRole] = await data.get_bundle_roles(bundle.id)

            field = ""
            has_allowed_roles = any(bundle_allowed_roles)
            has_roles = any(bundle_roles)

            if has_allowed_roles or has_roles:
                if has_roles:
                    field += "Roles:\n"
                    for bundle_role in bundle_roles:
                        field += f"> <@&{bundle_role.id}>\n"

                if has_allowed_roles:
                    field += "Allowed Roles:\n"
                    for bundle_allowed_role in bundle_allowed_roles:
                        field += f"> <@&{bundle_allowed_role.id}>\n"
            else:
                field = "No roles were allowed or added yet."

            embed.add_field(name=f"{i} | {bundle.name}", value=field, inline=False)
            i += 1

        return embed

    @try_func_async(embed=True)
    async def bundle_choices(self, allowed_roles: list[BundleRole]) -> Embed:
        data: 'Data'
        (data,) = self._get_cogs(include_data=True)

        embed = self.generate_embed("Role choices", f"These are the roles you have access to.", EmbedDefaults.WHITE)

        bundle_roles: list[int] = await data.get_bundles_choices(allowed_roles)

        field = ""
        i: int = 0
        for bundle_role in bundle_roles:
            field += f"`{i}` | <@&{bundle_role}>\n"
            i += 1

        embed.add_field(name="Available roles", value=field, inline=False)
        
        return embed

    #Debug
    def cog_restarted(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restarted", f"`{cog}` cog was successfully restarted.", color=EmbedDefaults.GREEN)

    def cog_restart_error(self, cog: str) -> Embed:
        return self.generate_embed("Cog Restart Failed", f"`{cog}` cog could not be restarted.")


def setup(bot):
    bot.add_cog(Embeds(bot))