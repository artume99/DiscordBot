import json
import discord
from discord.ext import commands, tasks
from Settings import *
from cogs.waiting_command import Waiting_room_txt, Waiting_room_id
import Utils


def get_prefix(client, message):
    with open("client_settings.json", 'r') as f:
        servers = json.load(f)
    return servers[str(message.guild.id)]["prefix"]


client = commands.Bot(command_prefix=get_prefix)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_guild_join(guild: discord.Guild):
    with open("client_settings.json", 'r') as f:
        servers = json.load(f)
    servers[str(guild.id)] = {}
    servers[str(guild.id)]["prefix"] = '/'
    servers[str(guild.id)]["waiting_room_name"] = "waiting-room"
    servers[str(guild.id)]["waiting_room_id"] = "786287417766182952"

    with open("client_settings.json", 'w') as f:
        json.dump(servers, f, indent=4)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Waiting'))
    print('Bot is ready')
    # await check_queue.start()


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # print(member, before, after)
    waiting_room_name, waiting_room_id = Utils.get_waiting_room_name_and_id(member.guild.id)
    if after.channel:
        if after.channel.name == waiting_room_name and before.channel.name != waiting_room_name:
            channel = client.get_channel(waiting_room_id)
            with open("client_settings.json", 'r') as f:
                servers = json.load(f)
            prefix = servers[str(member.guild.id)]["prefix"]
            await channel.send("welcome, please select {pre}autojoin or {pre}bymessage, (default is by message) "
                               "if you need help please ask your admins or read the "
                               "{pre}help".format(pre=prefix))


client.run(TOKEN)


"""
-------------------- EXAMPLES TO USE IN THE FUTURE IF NEEDED -----------------


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
"""