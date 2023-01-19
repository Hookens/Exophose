from discord.bot import Bot
from discord.commands import Option
from discord.commands.context import ApplicationContext
from discord.ext import commands
from discord.member import Member
import traceback

class UserCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Show Exophose's help.", guild_only=True)
    async def slash_help(self, ctx: ApplicationContext, submenu: Option(str, "Which help submenu to display", choices=["About", "Config", "Roles"], default="Roles"), bypassephemeral: Option(bool, "If you wish to make this message public, to show a command to a user for example.") = False):
        try:
            await ctx.interaction.response.defer(ephemeral=not bypassephemeral)

            helpmethods = self.bot.get_cog("Help")

            if helpmethods is not None:
                await ctx.interaction.followup.send(embed=await helpmethods.generate_help(submenu))
                
        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'slash_help', traceback.format_exc())

    @commands.slash_command(name="create", description="Assign yourself a custom role.", guild_only=True)
    async def slash_create(self, ctx: ApplicationContext, name: Option(str, "The name of the custom role you want.", required=True), color: Option(str, "The color of the custom role you want. Must be a hexadecimal color, hashtag is facultative.", required=True), badge: Option(str, "A link to an image file to set a badge.", required=False) = None):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if await verification.user_allowed(ctx.author):
                    await ctx.interaction.followup.send(embed=await methods.role_create(ctx, name, color, badge))
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_create', traceback.format_exc())

    @commands.slash_command(name="remove", description="Remove your custom role.", guild_only=True)
    async def slash_remove(self, ctx: ApplicationContext, index: Option(str, "The index of the custom role you want to delete. Use 'All' to delete all of your custom roles.", required=False) = None):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if await verification.user_allowed(ctx.author) :
                    if index is not None:
                        await ctx.interaction.followup.send(embed=await methods.role_remove(ctx.author, index))
                    else:
                        await ctx.interaction.followup.send(embed=await embeds.generate_embed_missing_index())
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_remove', traceback.format_exc())

    @commands.slash_command(name="recolor", description="Recolor your custom role.", guild_only=True)
    async def slash_recolor(self, ctx: ApplicationContext, color: Option(str, "The new color for your custom role.", required=True), index: Option(int, "The index of the custom role you want to recolor. Facultative if you only have one custom role.", required=False) = 0):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if await verification.user_allowed(ctx.author) :
                    await ctx.interaction.followup.send(embed=await methods.role_recolor(ctx, color, index))
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_recolor', traceback.format_exc())

    @commands.slash_command(name="rename", description="Rename your custom role.", guild_only=True)
    async def slash_rename(self, ctx: ApplicationContext, name: Option(str, "The new name for your custom role.", required=True), index: Option(int, "The index of the custom role you want to rename. Facultative if you only have one custom role.", required=False) = 0):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if await verification.user_allowed(ctx.author) :
                    await ctx.interaction.followup.send(embed=await methods.role_rename(ctx, name, index))
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_rename', traceback.format_exc())

    @commands.slash_command(name="rebadge", description="Update the badge on your custom role.", guild_only=True)
    async def slash_rebadge(self, ctx: ApplicationContext, badge: Option(str, "The image link for the new badge on your custom role. Put 'None' to remove it.", required=True), index: Option(int, "The index of the custom role you want to rebadge. Facultative if you only have one custom role.", required=False) = 0):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            methods = self.bot.get_cog("UserMethods")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and methods is not None and embeds is not None:
                if await verification.user_allowed(ctx.author) :
                    await ctx.interaction.followup.send(embed=await methods.role_rebadge(ctx, badge, index))
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_rebadge', traceback.format_exc())

    @commands.slash_command(name="created", description="List the created roles for a user.", guild_only=True)
    async def slash_created(self, ctx: ApplicationContext, member: Option(Member, "The user you wish to list the created roles for.", required=False) = None):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            embeds = self.bot.get_cog("Embeds")

            if embeds is not None:
                if member is not None :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_created_roles(member))
                else :
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_created_roles(ctx.author))

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_created', traceback.format_exc())

    @commands.slash_command(name="preview", description="Shows a color preview (if inputted) and a link to a colorpicker.", guild_only=True)
    async def slash_preview(self, ctx: ApplicationContext, color: Option(str, "The color you wish to preview.", required=False) = None):
        try:
            await ctx.interaction.response.defer(ephemeral=True)
            
            verification = self.bot.get_cog("Verification")
            embeds = self.bot.get_cog("Embeds")

            if verification is not None and embeds is not None:
                if await verification.user_allowed(ctx.author):
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_preview_color(ctx.author, color))
                else:
                    await ctx.interaction.followup.send(embed=await embeds.generate_embed_not_user_allowed())

        except Exception as e:
            logging = self.bot.get_cog("Logging")
            if logging is not None:
                await logging.log_error(e,'usercommands - slash_preview', traceback.format_exc())

def setup(bot):
    bot.add_cog(UserCommands(bot))