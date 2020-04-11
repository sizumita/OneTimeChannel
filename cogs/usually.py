from discord.ext import commands
import discord
ROLE_ID = 698313567757140048


class Usually(commands.Cog):
    """誰でも使用可能なコマンド"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def main(self, ctx):
        """メインチャンネル群へ接続します。"""
        role = ctx.guild.get_role(ROLE_ID)
        await ctx.author.add_roles(role)


def setup(bot):
    return bot.add_cog(Usually(bot))

