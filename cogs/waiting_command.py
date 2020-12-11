from discord.ext import commands, tasks
import discord
from typing import Dict, List
from Utils import *

Waiting_room = "waiting-room"
queue_to_rooms: Dict[discord.VoiceChannel, List[discord.Member]] = {}


def only_waiting_channel():
    def predicate(ctx: commands.Context):
        channel = ctx.channel
        return channel.name == Waiting_room

    return commands.check(predicate)


async def back_to_room(member: discord.Member, room: discord.VoiceChannel):
    await member.move_to(room)


@tasks.loop(seconds=5)
async def check_queue():
    print(queue_to_rooms)
    for room in queue_to_rooms:
        if len(room.members) < room.user_limit:
            if len(queue_to_rooms[room]) > 0:
                await back_to_room(queue_to_rooms[room].pop(), room)


class Waiting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, ex):
        if type(ex) is commands.CheckFailure:
            await ctx.send("You can do this command only in the {w} text channel".format(w=Waiting_room))
        else:
            print(ex, type(ex))
            await ctx.send("Please check with /help the usage of this command")

    @commands.command()
    @only_waiting_channel()
    async def waitingfor(self, ctx: commands.Context, *, channel_name):
        voice_channel: List[discord.VoiceChannel]
        voice_channel = get_channel_from_name(ctx, channel_name)
        room = get_channel_from_name(ctx, Waiting_room)
        user: discord.Member = ctx.author
        if voice_channel not in queue_to_rooms:
            queue_to_rooms[voice_channel] = []
        queue_to_rooms[voice_channel].append(user)
        msg = discord.Embed(
            colour=discord.Colour.dark_gold()
        )
        msg.add_field(name='Player', value=str(user), inline=True)
        msg.add_field(name='For Room', value=channel_name, inline=True)
        msg.set_author(name='Waiting list')
        await ctx.send(embed=msg)
        await user.move_to(room)
        await check_queue.start()

    @commands.command()
    async def ash(self, ctx):
        await ctx.send("l")


def setup(bot: commands.Bot):
    bot.add_cog(Waiting(bot))
