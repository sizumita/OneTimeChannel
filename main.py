from bot import MyBot
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot = MyBot()

# extensions = ['cogs.operation', 'cogs.usually', 'cogs.watch', 'cogs.join_channel']
extensions = ['cogs.jinrou']

for extension in extensions:
    bot.load_extension(extension)

bot.run(os.environ.get("TOKEN"))
