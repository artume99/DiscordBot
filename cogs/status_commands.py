import discord
from discord.ext import commands, tasks
import Utils


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx: commands.Context):
        waiting = self.bot.cogs["Waiting"]
        q = waiting.get_q()
        user_to_room = waiting.get_user_to_room()
        member = ctx.author
        room = user_to_room[member]
        place = q[room].index(member) + 1
        await ctx.send(f"You are in {place} place")

    @commands.command()
    async def stam(self, ctx):
        channel = discord.utils.get(ctx.guild.text_channels, name="waiting-room")
        channel_id = channel.id
        await ctx.send(channel_id)

    @commands.command()
    async def autojoin(self, ctx: commands.Context):
        waiting = self.bot.cogs["Waiting"]
        q = waiting.get_auto_msg()
        member = ctx.author
        q[member] = False

    @commands.command(aliases=['msg'])
    async def bymessage(self, ctx: commands.Context):
        waiting = self.bot.cogs["Waiting"]
        q = waiting.get_auto_msg()
        member = ctx.author
        q[member] = True


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
