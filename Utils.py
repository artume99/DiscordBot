from typing import List
import discord


def get_channel_from_name(ctx, name) -> List[discord.VoiceChannel]:
    return discord.utils.get(ctx.guild.voice_channels, name=name)


