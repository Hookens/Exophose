from discord.bot import Bot
from discord.ui import Button
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import View
from discord.member import Member
import traceback

ICONURLBOT = "YOUR URL"

class UserLegacy(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="preview")
    async def command_preview(self, ctx: Context, color: str = None):
        try:
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        await ctx.send(embed=await embeds.generate_embed_preview_color(ctx.author, color))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_preview', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="create")
    async def command_create(self, ctx: Context, name: str = None, color: str = None):
        try:
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        if name is not None and color is not None:
                                await ctx.send(embed=await methods.role_create(ctx, name, color))
                        else:
                            await ctx.send(embed=await embeds.generate_embed('Missing arguments', f"Command `create` requires a name and a hexadecimal color code.\nE.g. `exo create \"Very Bombastic\" #FF8C00`"))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_create', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="remove")
    async def command_remove(self, ctx: Context, index: str = None):
        try:
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        if index is not None:
                            await ctx.send(embed=await methods.role_remove(ctx.author, index))
                        else:
                            await ctx.send(embed = await embeds.generate_embed_missing_index())
                        
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_remove', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="rename")
    async def command_rename(self, ctx: Context, name: str = None, index: str = 0):
        try:
            verification = self.bot.get_cog("Verification")
            utilities = self.bot.get_cog("Utilities")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and utilities is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        if name is not None:
                            if utilities.parsable_int(index):
                                await ctx.send(embed=await methods.role_rename(ctx, name, int(index)))
                            else:
                                await ctx.send(embed=await embeds.generate_embed_int_parsing_error(index))
                        else:
                            await ctx.send(embed=await embeds.generate_embed('Missing arguments', f"Command `rename` requires a name.\nE.g. `exo rename \"Vroom Vroom\"`"))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_rename', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="recolor")
    async def command_recolor(self, ctx: Context, color: str = None, index: str = 0):
        try:
            verification = self.bot.get_cog("Verification")
            utilities = self.bot.get_cog("Utilities")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and utilities is not None and methods is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        if color is not None:
                            if utilities.parsable_int(index):
                                    await ctx.send(embed=await methods.role_recolor(ctx, color, int(index)))
                            else:
                                await ctx.send(embed=await embeds.generate_embed_int_parsing_error(index))
                        else:
                            await ctx.send(embed=await embeds.generate_embed('Missing arguments', f"Command `recolor` requires a color.\nE.g. `exo recolor #CC0000`"))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_recolor', traceback.format_exc())

    @commands.guild_only()
    @commands.command(name="created")
    async def command_created(self, ctx: Context, member: Member = None):
        try:
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and embeds is not None:
                if not verification.has_channel_permission(ctx.guild, ctx.channel, 1):
                    return
                    
                elif not verification.has_channel_permission(ctx.guild, ctx.channel, 2):
                    await ctx.send(content="Exophose requires the `Embed_Links` permission.")
                
                else:
                    if await verification.user_allowed(ctx.author):
                        if member is not None :
                            await ctx.send(embed=await embeds.generate_embed_created_roles(member))
                        else :
                            await ctx.send(embed=await embeds.generate_embed_created_roles(ctx.author))
                    else:
                        await ctx.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'userlegacy - command_created', traceback.format_exc())

def setup(bot):
    bot.add_cog(UserLegacy(bot))