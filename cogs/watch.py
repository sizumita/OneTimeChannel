from discord.ext import commands
import discord
from cogs.utils.texts import greeting_message, first_message
GUILD_INVITE = "https://discord.gg/qCKy9va"
LOG_CHANNEL = 698300390449348617


class Watch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.reset())
        self.greeting_message_id = None

    async def reset(self):
        await self.bot.wait_until_ready()
        greeting_channel = self.bot.get_channel(698300559031140464)
        await greeting_channel.purge()
        msg = await greeting_channel.send(greeting_message)
        self.greeting_message_id = msg.id
        await msg.add_reaction('\U0001f44d')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def create_channel(self, payload: discord.RawReactionActionEvent):
        """チャンネルを作成する"""
        if payload.message_id != self.greeting_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            return
        reactioned_message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
        category = guild.get_channel(698300310669754369)
        topic = f'{member.id}'
        ov = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        channel = await category.create_text_channel(name=member.name, overwrites={member: ov}, topic=topic)
        invite = await channel.create_invite()
        embed = first_message(member)
        msg = await channel.send(embed=embed)
        self.bot.invites[invite.id] = invite.uses
        await channel.send(f'招待url: {invite.url}')
        await msg.pin()
        await reactioned_message.remove_reaction('\U0001f44d', member)
        log = self.bot.get_channel(LOG_CHANNEL)
        await log.send(f'{member.mention}がチャンネルを作成しました！')

    @commands.Cog.listener(name='on_member_join')
    async def join(self, member):
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
        topic = channel.topic.split()
        if len(topic) == 2:
            if topic[1] != '-1':
                if inv.uses >= int(topic[1]):
                    await member.send(f'申し訳ありませんが、チャンネル作成者が設定した人数制限によって入室することができませんでした。')
                    return

        ov = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        await channel.set_permissions(member, overwrite=ov)
        await channel.send(f'{member.mention}さんが入室しました。')

    @commands.Cog.listener(name='on_message')
    async def dm_join(self, message):
        if isinstance(message.channel, discord.DMChannel):
            if message.content.startswith('http://discord.gg/'):
                guild = self.bot.get_guild(698296192152502274)
                for invite in await guild.invites():
                    if invite.url == message.content:
                        channel = invite.channel
                        if invite.url == GUILD_INVITE:
                            return
                        topic = channel.topic.split()
                        if len(topic) == 2:
                            if topic[1] != '-1':
                                if invite.uses >= int(topic[1]):
                                    await message.author.send(f'申し訳ありませんが、チャンネル作成者が設定した人数制限によって入室することができませんでした。')
                                    return
                        member = guild.get_member(message.author.id)
                        ov = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                        await channel.set_permissions(member, overwrite=ov)
                        await channel.send(f'{member.mention}さんが入室しました。')
                        return


def setup(bot):
    return bot.add_cog(Watch(bot))
