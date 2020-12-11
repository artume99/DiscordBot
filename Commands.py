from discord.ext import commands
from Bot import TOKEN

client = commands.Bot(command_prefix='/')
client.run(TOKEN)