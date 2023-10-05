from django.shortcuts import render
from django.http import JsonResponse
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo
import json

def getPlayerByName(request, pk):

    try:

        player_list = players.find_players_by_full_name(pk)
        active_players = [player for player in player_list if player['is_active']]

        if active_players:

            base_url = 'https://cdn.nba.com/headshots/nba/latest/1040x760/'

            for player in active_players:
                player_id = player['id']
                player['image_url'] = f'{base_url}{player_id}.png'
                player_details = getPlayerDetails(player_id)
                player.update(player_details)

            return JsonResponse({'players': active_players})
        
        else:
            return JsonResponse({'error': 'Players not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)       


def getPlayerDetails(player_id):

    playerDetails = commonplayerinfo.CommonPlayerInfo(player_id=player_id) 
    player_json = playerDetails.get_json()
    player_dict = json.loads(player_json)
    player_info = player_dict['resultSets'][0]['rowSet'][0]
    team_city = player_info[22]
    team_name = player_info[19]
    height = player_info[11]
    weight = player_info[12]
    position = player_info[15]

    player_extra_info = player_dict['resultSets'][1]['rowSet'][0]
    points = player_extra_info[3]
    assists = player_extra_info[4]
    rebounds = player_extra_info[5]

    return {
        'team_city': team_city,
        'team_name': team_name,
        'height': height,
        'weight': weight,
        'position': position,
        'points': points,
        'assists': assists,
        'rebounds': rebounds,
    }

