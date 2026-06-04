from typing import Sequence
from models.player_manager import PlayerManager


def get_member_info(guild_members: Sequence):
    player_manager = PlayerManager()

    for member in guild_members:
        if not member.bot:
            player_manager.members.append(member.display_name)

        if member.activity is not None:
            player_manager.online_members[member.id] = {
                'display_name': member.display_name,
                'id': member.id,
                'activity': member.activity.name,
            }

    for player_info in player_manager.online_members.values():

        activity = player_info['activity']

        if activity not in player_manager.activity_count:
            player_manager.activity_count[activity] = 1
        else:
            player_manager.activity_count[activity] += 1


    display_names = [
        player_info['display_name']
        for player_info in player_manager.online_members.values()
    ]


    return player_manager

