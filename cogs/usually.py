from discord.ext import commands
import discord
ROLE_ID = 698313567757140048


class Usually(commands.Cog):
    """誰でも使用可能なコマンド"""
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.channel.category:
            return False
        if ctx.channel.category.id == 698300310669754369:
            if ctx.channel.topic == "[GAME]":
                return False
            return True

        return False

    @commands.command()
    async def main(self, ctx):
        """メインチャンネル群へ接続します。"""
        role = ctx.guild.get_role(ROLE_ID)
        await ctx.author.add_roles(role)

    @commands.command()
    async def leave(self, ctx):
        """チャンネルから去ります。"""
        if ctx.channel.topic.split()[0] == str(ctx.author.id):
            return
        ov = discord.PermissionOverwrite(read_messages=False, send_messages=False)
        await ctx.channel.set_permissions(ctx.author, overwrite=ov)
        await ctx.channel.send(f'{ctx.author}さんが退出しました。')
        return


def setup(bot):
    return bot.add_cog(Usually(bot))

