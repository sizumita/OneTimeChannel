from discord.ext import commands
import discord


class Operation(commands.Cog):
    """
    チャンネル作成者のみが使用可能なコマンドです。
    """
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.channel.category:
            return False

        if ctx.channel.category.id == 698300310669754369:
            if ctx.channel.topic.split()[0] == str(ctx.author.id):
                return True

        return False

    @commands.command(aliases=['remove'])
    async def delete(self, ctx):
        """チャンネルを削除します。チャンネル作成者のみ使用可能です。"""
        invites = await ctx.channel.invites()
        for invite in invites:
            await invite.delete()

        topic = ctx.channel.topic.split()
        if len(topic) == 3 and topic[2] != '-1':
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
        topic = ctx.channel.topic.split()
        if len(topic) != 3 or topic[2] != '-1':
            voice = ctx.guild.get_channel(int(topic[2]))
            if voice:
                await ctx.send("既に存在します")
                return
        ov = discord.PermissionOverwrite(speak=True, connect=True, view_channel=True)
        discord.Permissions.voice()
        voice = await ctx.channel.category.create_voice_channel(name=ctx.channel.name)
        if len(topic) == 1:
            topic += ['-1', str(voice.id)]
        elif len(topic) == 2:
            topic += [str(voice.id)]
        else:
            topic[2] = str(voice.id)
        await ctx.channel.edit(topic='\n'.join(topic))

        for member in ctx.channel.members:
            await voice.set_permissions(member, overwrite=ov)
        await ctx.send('作成されました。')


def setup(bot):
    return bot.add_cog(Operation(bot))
