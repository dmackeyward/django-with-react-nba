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
                
            print("active players", active_players)
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










    # player = commonplayerinfo.CommonPlayerInfo(player_id='2544') 
    # lebron_json = lebron.get_json()
    # lebron_dict = json.loads(lebron_json)
    # # Retrieve data for LeBron James
    # lebron_info = lebron_dict['resultSets'][0]['rowSet'][0]
    # # Access different fields using the appropriate indices
    # team_city = lebron_info[22]  # Team City
    # team_name = lebron_info[19]  # Team Name
    # height = lebron_info[11]     # Heightc
    # weight = lebron_info[12]     # Weight
    # position = lebron_info[15]
    # print("TEAM CITY:", team_city)
    # print("TEAM NAME:", team_name)
    # print("HEIGHT:", height)
    # print("WEIGHT:", weight)
    # print("POSITION:", position)
    # lebron_info1 = lebron_dict['resultSets'][1]['rowSet'][0]
    # print(lebron_info1)
    # points = lebron_info1[3]     # Points (PTS)
    # assists = lebron_info1[4]    # Assists (AST)
    # rebounds = lebron_info1[5]   # Rebounds (REB)
    # print("POINTS:", points)
    # print("ASSISTS:", assists)
    # print("REBOUNDS:", rebounds)









    # try:

    #     player_list = players.find_players_by_full_name(pk)
    #     active_players = [player for player in player_list if player['is_active']]

    #     if active_players:

    #         base_url = 'https://cdn.nba.com/headshots/nba/latest/1040x760/'

    #         for player in active_players:
    #             player_id = player['id']
    #             player['image_url'] = f'{base_url}{player_id}.png'

    #         print("active players", active_players)
    #         return JsonResponse({'players': active_players})
        
    #     else:
    #         return JsonResponse({'error': 'Players not found'}, status=404)

    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)



