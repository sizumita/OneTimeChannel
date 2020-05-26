from discord.ext import commands
import discord
from cogs.utils.topic import set_voice_channel, get_voice_channel_id


class Operation(commands.Cog):
    """
    チャンネル作成者のみが使用可能なコマンドです。
    """
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if ctx.channel.category:
            return False

        if ctx.channel.topic.split()[0] == str(ctx.author.id):
            return True

        return False

    @commands.command(aliases=['remove'])
    async def delete(self, ctx):
        """チャンネルを削除します。チャンネル作成者のみ使用可能です。"""
        invites = await ctx.channel.invites()
        for invite in invites:
            await invite.delete()

        topic = ctx.channel.topic.split('\n')
        if topic[2] != '-1':
            voice = ctx.guild.get_channel(int(topic[2]))
            if voice:
                await voice.delete()

        await ctx.channel.delete()

    @commands.command()
    async def everyone(self, ctx):
        """everyoneメンションを送信します。"""
        await ctx.send('@everyone')

    @commands.command()
    async def here(self, ctx):
        """hereメンションを送信します。"""
        await ctx.send('@here')

    @commands.command()
    async def limit(self, ctx, count: int):
        """チャンネルに参加できる最大人数を制限します。-1にすると無効化されます。"""
        topic = ctx.channel.topic.split()
        if len(topic) == 1:
            topic.append(str(count))
        else:
            topic[1] = str(count)

        await ctx.channel.edit(topic="\n".join(topic))
        await ctx.send('設定しました。')

    @commands.command()
    async def name(self, ctx, name):
        """チャンネル名を変更します。"""
        await ctx.channel.edit(name=name)
        topic = ctx.channel.topic.split()
        if topic[2] != '-1':
            voice = ctx.guild.get_channel(int(topic[2]))
            if voice:
                await voice.edit(name=name)
        await ctx.send('設定しました。')

    @commands.command()
    async def nsfw(self, ctx):
        """チャンネルをnsfwにします。"""
        if ctx.channel.nsfw:
            await ctx.channel.edit(nsfw=False)
            return
        await ctx.channel.edit(nsfw=True)
        await ctx.send('設定しました。')

    @commands.command()
    async def voice(self, ctx):
        """ボイスチャンネルを作成します"""
        if voice_id := get_voice_channel_id(ctx.channel.topic):
            voice = ctx.guild.get_channel(voice_id)
            if voice is not None:
                await ctx.send("既に存在します")
                return
        ov = discord.PermissionOverwrite(speak=True, connect=True, view_channel=True)
        voice = await ctx.channel.guild.create_voice_channel(name=ctx.channel.name)
        await ctx.channel.edit(topic=set_voice_channel(voice.id, ctx.channel.topic))

        for member in ctx.channel.members:
            await voice.set_permissions(member, overwrite=ov)
        await ctx.send('作成されました。')

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        """チャンネルからメンバーを退出させます。"""
        ov = discord.PermissionOverwrite(read_messages=False)
        voice_ov = discord.PermissionOverwrite(speak=False, connect=False, view_channel=False)
        if voice_id := get_voice_channel_id(ctx.channel.topic):
            voice = ctx.guild.get_channel(voice_id)
            if voice is not None:
                await voice.set_permissions(target=member, overwrite=voice_ov)
        await ctx.channel.set_permissions(target=member, overwrite=ov)
        await ctx.send(f'ユーザー: {member} を退出させました。')

    @commands.command()
    @commands.cooldown(1, 60.0)
    async def refresh(self, ctx):
        """チャンネルの招待を変更します。"""
        for invite in await ctx.channel.invites():
            await invite.delete()
        invite = await ctx.channel.create_invite()
        self.bot.invites[invite.id] = invite.uses
        msg = await ctx.send(f'新規招待url: {invite.url}')
        await msg.pin()


def setup(bot):
    return bot.add_cog(Operation(bot))
