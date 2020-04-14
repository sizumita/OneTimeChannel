from discord.ext import commands
import discord
import re
GUILD_INVITE = "https://discord.gg/qCKy9va"
LOG_CHANNEL = 698300390449348617
invite_text = """
[チャンネルの招待]
{}
このチャンネルに入る場合は \U0001f44d リアクションを押してください。
"""


class JoinChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def join_channel(self, channel, invite, member):
        topic = channel.topic.split()
        if len(topic) == 2:
            if topic[1] != '-1':
                if invite.uses >= int(topic[1]):
                    await member.send(f'申し訳ありませんが、チャンネル作成者が設定した人数制限によって入室することができませんでした。')
                    return

        ov = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        await channel.set_permissions(member, overwrite=ov)
        await channel.send(f'{member.mention}さんが入室しました。')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def join_channel_by_reaction(self, payload: discord.RawReactionActionEvent):
        """リアクションからチャンネルへ入る"""
        if str(payload.emoji) != "\U0001f44d":
            return
        channel = self.bot.get_channel(payload.channel_id)
        member = channel.guild.get_member(payload.user_id)
        message = await channel.fetch_message(payload.message_id)

        if not message.author.id == self.bot.user.id:
            return
        if member.bot:
            return
        if not message.content.startswith("[チャンネルの招待]"):
            return

        invite_url = message.content.split('\n')[1]
        for invite in await message.guild.invites():
            if invite.url == invite_url:
                await self.join_channel(invite.channel, invite, member)

    @commands.Cog.listener(name='on_member_join')
    async def join(self, member):
        """招待urlから入る"""
        inv = None
        for invite in await member.guild.invites():
            if invite.url == GUILD_INVITE:
                continue
            if invite.id not in self.bot.invites.keys():
                self.bot.invites[invite.id] = invite.uses
                continue
            if self.bot.invites[invite.id] != invite.uses:
                self.bot.invites[invite.id] += 1
                inv = invite

        channel = inv.channel
        if inv.url == GUILD_INVITE:
            return

        await self.join_channel(channel, inv, member)

    @commands.Cog.listener(name='on_message')
    async def dm_check(self, message):
        """DMに送られた招待urlから入る"""
        if isinstance(message.channel, discord.DMChannel):
            guild = self.bot.get_guild(698296192152502274)
            if invite_id_list := re.findall(r'.*discord\.gg/(.{7}).*', message.content):
                invites = [inv for inv in await guild.invites() if inv.id in invite_id_list]
                for invite in invites:
                    channel = invite.channel
                    if invite.url == GUILD_INVITE:
                        return
                    member = guild.get_member(message.author.id)
                    await self.join_channel(channel, invite, member)