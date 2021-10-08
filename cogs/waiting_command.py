from discord.ext import commands, tasks
import discord
from typing import Dict, List
from Utils import *

Waiting_room_txt = "waiting-room"
Waiting_room_id = 786287417766182952
queue_to_rooms: Dict[discord.VoiceChannel, List[discord.Member]] = {}
user_to_room: Dict[discord.Member, discord.VoiceChannel] = {}
auto_or_message: Dict[discord.Member, bool] = {}  # True-message, False-auto
can_come_back: Dict[discord.Member, int] = {}


def only_waiting_channel():
    def predicate(ctx: commands.Context):
        channel = ctx.channel
        waiting_room_name, waiting_room_id = get_waiting_room_name_and_id(ctx.guild.id)
        return channel.name == waiting_room_name

    return commands.check(predicate)


class Waiting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def back_to_room(self, members: List[discord.Member], room: discord.VoiceChannel):
        member = members.pop(0)
        try:
            waiting_room_name, waiting_room_id = get_waiting_room_name_and_id(room.guild.id)
            if member.voice.channel.name == waiting_room_name:
                if can_come_back[member] <= 2:
                    if auto_or_message[member]:
                        await member.send("Your turn to join {room}".format(room=room))
                    else:
                        await member.move_to(room)
                    if can_come_back[member] <= 2:
                        await self.back_waiting.start(member)
        except discord.errors.HTTPException:
            await member.send("Your turn to join {room}".format(room=room))
            if can_come_back[member] <= 3:
                await self.back_waiting.start(member)

    @tasks.loop(count=3, seconds=5)  # Change to 20
    async def back_waiting(self, member: discord.Member):
        can_come_back[member] += 1
        print(can_come_back)
        print("back waiting")
        try:
            waiting_room_name, waiting_room_id = get_waiting_room_name_and_id(member.guild.id)
            if member.voice.channel.name == waiting_room_name:
                room = user_to_room[member]
                queue_to_rooms[room].insert(0, member)
                can_come_back[member] = 0
        except discord.errors.HTTPException:
            await member.send("You left the channel and lost your turn")

    @tasks.loop(seconds=5)  # Change for every 10 seconds
    async def check_queue(self):
        print(queue_to_rooms)
        for room in queue_to_rooms:
            if len(room.members) < room.user_limit:
                if len(queue_to_rooms[room]) > 0:
                    await self.back_to_room(queue_to_rooms[room], room)

    @check_queue.before_loop
    async def before_queue(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, ex):
        waiting_room_name, waiting_room_id = get_waiting_room_name_and_id(ctx.guild.id)
        print(ex, type(ex))
        if type(ex) is commands.CheckFailure:
            await ctx.send("You can do this command only in the {w} text channel".format(w=waiting_room_name))
        elif type(ex) is discord.ext.commands.errors.CommandInvokeError:
            await ctx.send("User not found")
        else:
            print(ex, type(ex))
            await ctx.send("Please check with /help the usage of this command")

    @commands.command()
    @only_waiting_channel()
    async def waitingfor(self, ctx: commands.Context, *, channel_name):
        print("here")
        voice_channel: List[discord.VoiceChannel]
        voice_channel = get_channel_from_name(ctx, channel_name)
        waiting_room_name, waiting_room_id = get_waiting_room_name_and_id(ctx.guild.id)
        room = get_channel_from_name(ctx, waiting_room_name)
        user: discord.Member = ctx.author
        if voice_channel not in queue_to_rooms:
            queue_to_rooms[voice_channel] = []
        if user in queue_to_rooms[voice_channel]:
            return
        user_to_room[user] = voice_channel
        auto_or_message[user] = True
        can_come_back[user] = 0
        self.check_queue.cancel()
        await self.bot.wait_until_ready()
        queue_to_rooms[voice_channel].append(user)
        msg = discord.Embed(
            colour=discord.Colour.dark_gold()
        )
        msg.add_field(name='Player', value=str(user), inline=True)
        msg.add_field(name='For Room', value=channel_name, inline=True)
        msg.set_author(name='Waiting list')
        await ctx.send(embed=msg)
        await user.move_to(room)
        await self.check_queue.start()

    @commands.command()
    async def ash(self, ctx):
        await ctx.send("l")

    def get_q(self):
        return queue_to_rooms

    def get_user_to_room(self):
        return user_to_room

    def get_auto_msg(self):
        return auto_or_message


def setup(bot: commands.Bot):
    bot.add_cog(Waiting(bot))
