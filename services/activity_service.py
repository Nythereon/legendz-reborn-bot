import json
from typing import Sequence
from models.player_manager import PlayerManager


def get_member_info(guild_members: Sequence):
    player_manager = PlayerManager()

    try:
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

    except Exception as error:
        player_manager.online_members['error'] = str(error)

    finally:
        display_names = [
            player_info['display_name']
            for player_info in player_manager.online_members.values()
        ]

        print(f'Total Members: {player_manager.total_count}')
        print(f'Online Members: {player_manager.online_count}')
        print(display_names)
        print('')
        print(f'Games Being Played')
        print(json.dumps(player_manager.activity_count))
        print('')
    return player_manager

