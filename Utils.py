from typing import List
import json
import discord


def get_channel_from_name(ctx, name) -> List[discord.VoiceChannel]:
    return discord.utils.get(ctx.guild.voice_channels, name=name)


def get_waiting_room_name_and_id(server_id):
    with open("client_settings.json", 'r') as f:
        servers = json.load(f)
    return servers[str(server_id)]["waiting_room_name"], servers[str(server_id)]["waiting_room_id"]
