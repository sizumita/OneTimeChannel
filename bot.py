from discord.ext import commands
import discord

GUILD_INVITE = "https://discord.gg/qCKy9va"


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__('/')
        self.invites = {}

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CheckFailure):
            return
        await super().on_command_error(context, exception)

    async def on_ready(self):
        guild = self.get_guild(698296192152502274)
        for invite in await guild.invites():
            self.invites[invite.id] = invite.uses


