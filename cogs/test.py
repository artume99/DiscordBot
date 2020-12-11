import discord
from discord.ext import commands

client = commands.Bot(command_prefix='/')

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.command()
    # async def ping(self, ctx: commands.Context):
    #     await ctx.send("Pong")

def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))

