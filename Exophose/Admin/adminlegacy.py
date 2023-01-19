from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ui import Button
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import View
from discord.member import Member
from discord.role import Role
import traceback

class AdminLegacy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="allow")
    async def command_allow(self, ctx: Context, role: Role = None, maxroles: int = 1, allowbadges: bool = False):
        try:
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("AdminMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if ctx.author.guild_permissions.administrator:
                        if role is not None :
                            await ctx.send(embed=await methods.allow_role(role, ctx, maxroles, allowbadges))
                        else:
                            await ctx.send(embed=await embeds.generate_embed('Missing arguments', f"Command `allow` requires a role.\nE.g. `exo allow @Supporters`"))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_admin_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'AdminLegacy - command_allow', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="disallow")
    async def command_disallow(self, ctx: Context, role: Role = None):
        try:
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("AdminMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if ctx.author.guild_permissions.administrator:
                        if role is not None :
                            await ctx.send(embed=await methods.disallow_role(role, ctx))
                        else:
                            await ctx.send(embed=await embeds.generate_embed('Missing arguments', f"Command `disallow` requires a role.\nE.g. `exo disallow @Patrons`"))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_admin_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'AdminLegacy - command_disallow', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="allowed")
    async def command_allowed(self, ctx: Context):
        try:
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if ctx.author.guild_permissions.administrator:
                        await ctx.send(embed=await embeds.generate_embed_allowed_roles(ctx.guild.id))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_admin_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'AdminLegacy - command_allowed', traceback.format_exc())


def setup(bot):
    bot.add_cog(AdminLegacy(bot))