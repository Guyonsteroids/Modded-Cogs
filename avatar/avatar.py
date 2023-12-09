import discord
from redbot.core import app_commands, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, error
from typing import Optional

_ = Translator("Avatar", __file__)

@cog_i18n(_)
class Avatar(commands.Cog):
    """Get a user's avatar."""

    @commands.hybrid_command(name="avatar", description="Get a user's avatar")
    @app_commands.describe(user="The user you wish to retrieve the avatar of")
    @app_commands.guild_only()
    async def avatar(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Returns a user's avatar as attachment. Defaults to requester when no argument is supplied."""
        user = user or ctx.author
        message = _("Your avatar") if user == ctx.author else _("{name}'s avatar").format(name=bold(user.display_name))
        
        if ctx.channel.permissions_for(ctx.guild.me).attach_files or ctx.channel.permissions_for(ctx.guild.me).embed_links:
            
            pfp = user.avatar if isinstance(ctx.channel, discord.channel.DMChannel) else user.display_avatar
            file_ext = "gif" if pfp and pfp.is_animated() else "png"
            embed = discord.Embed(description=message)
            embed.set_image(url=f"attachment://pfp-{user.id}.{file_ext}")
            return await ctx.send(file=await pfp.to_file(filename=f"pfp-{user.id}.{file_ext}"), embed=embed)

        await ctx.send(error(_("I do not have permission to attach files or embed links in this channel.")), ephemeral=True)

    async def red_delete_data_for_user(self, **kwargs) -> None:
        pass
