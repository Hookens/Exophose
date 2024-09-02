from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async
from Utilities.constants import HelpDefaults, AdminTexts, UserTexts, BundleTexts


class HelpMethods(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def generate_help(self, menu: str = "") -> Embed:
        if menu == HelpDefaults.HELP_OPTIONS[1]:
            embed = self.generate_help_custom_roles()
        elif menu == HelpDefaults.HELP_OPTIONS[2]:
            embed = self.generate_help_bundle_roles()
        elif menu == HelpDefaults.HELP_OPTIONS[3]:
            embed = self.generate_help_custom_configuration()
        elif menu == HelpDefaults.HELP_OPTIONS[4]:
            embed = self.generate_help_bundle_configuration()
        else:
            embed = self.generate_help_about_exophose()

        embed.color = HelpDefaults.COLOR
        author = self.bot.get_user(HelpDefaults.AUTHOR)
        embed.set_footer(text=f"Developed by {author.name}", icon_url=author.avatar.url)
        return embed

    def generate_help_about_exophose(self):
        embed = Embed(title="About Exophose", description="Exophose is a simple role management bot that allows users to create custom roles for themselves and/or select roles from bundles, depending on the configuration. It is intended as a reward system, not for role menus.\n\nSupporting my work is entirely optional. All features are always available.")

        embed.add_field(name="Support server", value=HelpDefaults.SUPPORT_SERVER, inline=True)
        embed.add_field(name="Invite Exophose", value=HelpDefaults.APP_DIRECTORY, inline=True)
        embed.add_field(name="Support my work", value=HelpDefaults.SUPPORT_ME, inline=True)

        embed.add_field(name="Custom Configuration", value="Configure what roles have access to complete customization.", inline=False)
        embed.add_field(name="Bundle Configuration", value="Configure bundles, what roles are allowed to use them, and what roles they offer.", inline=False)
        embed.add_field(name="Custom Roles", value="Manage your custom roles", inline=False)
        embed.add_field(name="Bundle Roles", value="Choose bundle roles", inline=False)
        embed.add_field(name="Limitations", value="Discord limits roles to 250 per server, plan ahead accordingly.", inline=False)

        return embed
    
    def generate_help_custom_configuration(self):
        embed = Embed(title="Custom  •  Configuration", description="Commands for configuration of access to complete customization.")

        commands: str = (
            f"</allow:1034567444758536214> - {AdminTexts.C_ALLOW}\n"
            f"</disallow:1034567444758536215> - {AdminTexts.C_DISALLOW}\n"
            f"</allowed:1034567444758536216> - {AdminTexts.C_ALLOWED}\n"
        )
        tips: str = (
            "- The maximum roles and whether or not a role allows badges can be edited by re-allowing it.\n"
            "- A maximum of 20 roles can be allowed."
        )
        
        embed.add_field(name="Commands", value=commands, inline=False)
        embed.add_field(name="Tips", value=tips, inline=False)

        return embed
        
    def generate_help_custom_roles(self):
        embed = Embed(title="Custom  •  Roles", description="Commands for custom role management.")

        commands: str = (
            f"</create:1034567444758536217> - {UserTexts.C_CREATE}\n"
            f"</created:1034567444758536221> - {UserTexts.C_CREATED}\n"
            f"</recolor:1034567444758536219> - {UserTexts.C_RECOLOR}\n"
            f"</rebadge:1039183332958806136> - {UserTexts.C_REBADGE}\n"
            f"</rename:1034567444758536220> - {UserTexts.C_RENAME}\n"
            f"</preview:1034567445115064420> - {UserTexts.C_PREVIEW}\n"
            f"</remove:1034567444758536218> - {UserTexts.C_REMOVE}\n"
        )
        tips : str = (
            "- Colors use hexadecimal format (#FFFFFF)."
        )

        embed.add_field(name="Commands", value=commands, inline=False)
        embed.add_field(name="Tips", value=tips, inline=False)

        return embed
    
    def generate_help_bundle_configuration(self):
        embed = Embed(title="Bundle  •  Configuration", description="Commands for configuration of access to bundles and their selection.")

        howto: str = (
            "How to bundle with Exophose:\n"
            "1. Create a bundle.\n"
            "2. Add roles to the bundle.\n"
            "3. Allow roles to use it.\n"
            "4. Profit."
        )
        commands: str = (
            f"</bundle create:1217257356795318382> - {BundleTexts.C_CREATE}\n"
            f"</bundle list:1217257356795318382> - {BundleTexts.C_LIST}\n"
            f"</bundle allow:1217257356795318382> - {BundleTexts.C_ALLOW}\n"
            f"</bundle disallow:1217257356795318382> - {BundleTexts.C_DISALLOW}\n"
            f"</bundle edit:1217257356795318382> - {BundleTexts.C_EDIT}\n"
            f"</bundle delete:1217257356795318382> - {BundleTexts.C_DELETE}\n"
        )
        tips : str = (
            "- A maximum of 5 bundles can be created.\n"
            "- A maximum of 10 roles can be allowed per bundle.\n"
            "- A maximum of 10 roles can be added per bundle."
        )

        embed.add_field(name="Setup", value=howto, inline=False)
        embed.add_field(name="Commands", value=commands, inline=False)
        embed.add_field(name="Tips", value=tips, inline=False)

        return embed
    
    def generate_help_bundle_roles(self):
        embed = Embed(title="Bundle  •  Roles", description="Commands for bundle role selection.")

        commands: str = (
            f"</bundle choices:1217225559202074744> - {BundleTexts.C_CHOICES}\n"
            f"</bundle choose:1217257356795318382> - {BundleTexts.C_CHOOSE}\n"
        )

        embed.add_field(name="Commands", value=commands, inline=False)

        return embed

def setup(bot):
    bot.add_cog(HelpMethods(bot))