from discord.ext import commands, tasks
import json
import discord
from typing import Dict, List
from Utils import *


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def changeprefix(self, ctx, prefix):
        with open("client_settings.json", 'r') as f:
            servers = json.load(f)
        servers[(str(ctx.guild.id))]["prefix"] = prefix

        with open("client_settings.json", 'w') as f:
            json.dump(servers, f, indent=4)

    @commands.is_owner()
    @commands.command()
    async def setwaitingroom(self, ctx: commands.Context, room):
        with open("client_settings.json", 'r') as f:
            servers = json.load(f)
        servers[(str(ctx.guild.id))]["waiting_room_name"] = room
        position = get_channel_from_name(ctx, room).position
        print(position)
        if not discord.utils.get(ctx.guild.text_channels, name="waiting-room"):
            await ctx.guild.create_text_channel("waiting-room-bot", position=position)
        channel = discord.utils.get(ctx.guild.text_channels, name="waiting-room")
        channel_id = channel.id
        servers[(str(ctx.guild.id))]["waiting_room_id"] = channel_id

        with open("client_settings.json", 'w') as f:
            json.dump(servers, f, indent=4)


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
