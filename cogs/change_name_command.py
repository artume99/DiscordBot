from discord.ext import commands, tasks
import json
import discord
from typing import Dict, List
from Utils import *

original_channel_names: Dict[discord.VoiceChannel, str] = {}


class ChangeName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def code(self, ctx: commands.Context, code):
        user = ctx.author
        channel = user.voice.channel
        name = channel.name
        if channel not in original_channel_names:
            original_channel_names[channel] = name
        name = original_channel_names[channel]
        print(f'{name} - {code}')
        await channel.edit(name=f'{name} - {code}')

    @commands.command()
    async def clearname(self, ctx: commands.Context):
        user = ctx.author
        channel = user.voice.channel
        name = original_channel_names[channel]
        await channel.edit(name=name)

    @commands.command(aliases=["c"])
    async def code1(self, ctx: commands.Context, code: str):
        user = ctx.author
        channel = user.voice.channel
        room_name = channel.name
        msg = discord.Embed(
            colour=discord.Colour.dark_gold()
        )
        msg.add_field(name='Code', value=code, inline=True)
        msg.add_field(name='For Room', value=room_name, inline=True)
        code_channel = discord.utils.get(ctx.guild.text_channels, name="code")
        await code_channel.send(embed=msg)

    @commands.command()
    async def bopo(self, ctx: commands.Context):
        user: discord.Member = ctx.author
        if user.display_name == "Bopo":
            channel = user.voice.channel
            await channel.edit(name="Bopo")


def setup(bot: commands.Bot):
    bot.add_cog(ChangeName(bot))
