import discord
import random


def notice(title, text):
    embed = discord.Embed(title=title, description=text, color=0x00bfff)
    return embed


def error(title, text):
    embed = discord.Embed(title=title, description=text, colour=discord.Colour("red"))
    return embed


class Game:
    def __init__(self, bot, master_id, main_channel_id, user_id_list):
        self.bot = bot
        self.master_id = master_id
        self.main_channel_id = main_channel_id
        self.user_id_list = user_id_list
        self.roles = {}
        self.started = False
        self.day = 1
        self.status = "night"
        self.wolf_channel_id = None
        self.dead = []

    def is_night(self):
        return True if self.status == "night" else False

    def set_role(self, roles):
        """
        :param roles: {role_name: count}
        role_nameの一覧
            normal: 村人
            wolf: 人狼
            teller: 占い師
            guard: 衛兵
            # 増えます
        :return: :bool:
        """
        users = self.user_id_list[:]
        random.shuffle(users)
        for role, count in roles.items():
            self.roles[role] = [i.id for i in users[:count]]
            users = users[count:]
        if users:
            return False
        return True

    async def start(self):
        if self.started:
            return
        self.started = True
        main_channel = self.bot.get_channel(self.main_channel_id)
        await main_channel.send(embed=notice('ゲームを開始します！', text=f'{self.day}日目の夜を開始します。\n人狼は殺すことはできません。'))
        await main_channel.send(embed=notice('チャンネル作成情報', '人狼専用チャンネルを作成します...'))
        guild = main_channel.guild
        ov = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        wolf_channel = await main_channel.category.create_text_channel(name='人狼用チャンネル')
        for x in self.roles['wolf']:
            await wolf_channel.set_permissions(guild.get_member(x), overwrite=ov)
        self.wolf_channel_id = wolf_channel.id
        await self.start_night(can_wolf_kill=False)

    async def start_night(self, can_wolf_kill=True):
        main_channel = self.bot.get_channel(self.main_channel_id)
        wolf_channel = self.bot.get_channel(self.wolf_channel_id)
        await main_channel.send(embed=notice(f'{self.day}日目の夜が始まりました！', '行動を開始します...'))
        if can_wolf_kill:
            await main_channel.send(embed=notice('人狼が殺します', '人狼専用チャンネルにて捕食する議論をしてください。'))
            user_list = [self.bot.get_user(i).mention for i in [users for role, users in self.roles.items() if role.name != 'wolf']]
            await wolf_channel.send(embed=notice('以下の中から捕食するユーザーを選択してください。全員が/kill [名前,メンション,ユーザーid]と入れると殺せます。', '\n'.join(user_list)))

    async def start_day(self):
        pass
