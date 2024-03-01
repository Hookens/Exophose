from discord.bot import Bot
from discord.embeds import Embed
from discord.ext import commands

from Debug.debughelpers import try_func_async

WHITE = 0xFFFFFF
AUTHOR = 320214798640087040

class Help(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    #TODO: Proper help overhaul with views, dropdowns and buttons for decent navigation. Offer buttons where necessary to differentiate custom roles and bundles.

    @try_func_async(embed=True)
    async def generate_help(self) -> Embed:
        #if submenu == "Config":
        #    return await self.generate_help_config()
        #elif submenu == "About":
        #    return await self.generate_help_about()
        #else:
        return await self.generate_help_roles()

    @try_func_async(embed=True)
    async def generate_help_roles(self):
        embed = Embed(title="Help  •  Managing your roles", description="Here are the commands available to you to manage your custom roles.", colour=WHITE)
        embed.add_field(name="Feedback or issues?", value="[Join the support server!](https://discord.gg/dAabxGzned)", inline=True)
        embed.add_field(name="Enjoying the bot?", value="[Consider voting!](https://top.gg/bot/854906458344259615/vote)", inline=True)
        embed.add_field(name="Creating a custom role", value=">>> </create:1034567444758536217> `name:`French Fries `color:`#CC0000\nOptional: `badge:`[attachment]", inline=False)
        embed.add_field(name="Listing your roles and their indexes", value=">>> </created:1034567444758536221>\nOptional: `member:`<@320214798640087040>", inline=False)
        embed.add_field(name="Removing one or all your custom roles", value=">>> </remove:1034567444758536218> `index:`all", inline=False)
        embed.add_field(name="Renaming a custom role", value=">>> </rename:1034567444758536220> `name:`Frencher Friers\nOptional: `index:`0", inline=False)
        embed.add_field(name="Previewing a color to see if it matches", value=">>> </preview:1034567445115064420>\nOptional: `color:`58D6FF", inline=False)
        embed.add_field(name="Recoloring a custom role", value=">>> </recolor:1034567444758536219> `color:`F5267C\nOptional: `index:`2", inline=False)
        embed.add_field(name="Rebadging a custom role", value=">>> </rebadge:1039183332958806136> \nOptional: `badge:`[attachment] `index:`1", inline=False)
        embed.add_field(name="Various tips", value=">>>  **•**  Colors use hexadecimal format (#FFFFFF)\n  **•**  Indexes are set to 0 by default, except for </remove:1034567444758536218>.\n", inline=False)

        return embed

    @try_func_async(embed=True)
    async def generate_help_config(self):
        embed = Embed(title="Help  •  Configuring allowed roles", description="Here are the commands available to manage allowed roles.", colour=WHITE)
        embed.add_field(name="Allowing a role", value=">>> </allow:1034567444758536214> `role:`@Nitro Booster\nOptional: `max_roles:`1 `allow_badges:`False", inline=False)
        embed.add_field(name="Listing the allowed roles", value=">>> </allowed:1034567444758536216>\nOptional: `bypassephemeral:`False", inline=False)
        embed.add_field(name="Disallowing a role", value=">>> </disallow:1034567444758536215> `role:`@Nitro Booster", inline=False)
        embed.add_field(name="Various tips", value=">  **•**  You can edit the maximum roles and whether or not a role allows badges by re-allowing it.\n>  **•**  You can allow a maximum of 20 roles.", inline=False)

        return embed

    @try_func_async(embed=True)
    async def generate_help_about(self):
        embed = Embed(title="About Exophose", description="Exophose is a simple role management bot that allows users to create custom roles for themselves after they acquire a custom role.", colour=WHITE)
        embed.add_field(name="Feedback or issues?", value="[Join the support server!](https://discord.gg/dAabxGzned)", inline=True)
        embed.add_field(name="Enjoying the bot?", value="[Consider voting!](https://top.gg/bot/854906458344259615/vote)", inline=True)
        embed.add_field(name="Getting started", value=">  Take a look at the config help menu to get started.", inline=False)
        embed.add_field(name="Limitations", value="> Exophose is limited to 250 roles per server, plan ahead accordingly.", inline=False)

        author = self.bot.get_user(AUTHOR)
        embed.set_author(name=f"Developed by {author.display_name}", icon_url=author.avatar.url)

        return embed

def setup(bot):
    bot.add_cog(Help(bot))