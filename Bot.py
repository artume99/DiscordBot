from typing import List
import os
import discord
import queue
from discord.ext import commands, tasks
from typing import Dict
from itertools import cycle
from Settings import *
from cogs.waiting_command import back_to_room

# TOKEN = "NzgzNzc0MDM1ODYzNDA0NTc1.X8focw.KZCmuIlWQxZpScQfMiQ2F_H_m7w"
# status = cycle(['status 1', 'status 2'])
client = commands.Bot(command_prefix='/')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Waiting'))
    print('Bot is ready')
    # await check_queue.start()



client.run(TOKEN)

# async def create_channel(guild,channel_name):
#     category =

# @client.event
# async def on_member_join(member: discord.Member):
#     print(f'{member} has joined a server')
#
#
# @client.event
# async def on_member_remove(member: discord.Member):
#     print(f'{member} has left the server')
#
#
# @client.command()
# async def ping(ctx):
#     await ctx.send('Pong!')
#     print(type(ctx))
#
#
# @client.command(aliases=['8ball'])
# async def _8ball(ctx, *, question):
#     pass
#
#
# # ctx.channel <- channel object
# @client.command()
# async def kick(ctx, member: discord.Member, *, reason):
#     pass
#
#
# @client.command()
# async def unban(ctx: commands.Context, *, member):
#     banned_users = await ctx.guild.bans()
#
#
# @tasks.loop(seconds=10)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))
#
#
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('no arg')


# @commends.has_permission()
# @clear.error
