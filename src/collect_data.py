


import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import os

MLB_KEY = os.environ["MLB_KEY"]

def get_game_schedule():
    date_frmt = datetime.now().date().strftime('%Y/%m/%d')
    data = json.load(open('games_today.json'))
    # games_today_url = "http://api.sportradar.us/mlb/trial/v6.5/en/games/{}/boxscore.json?api_key={}".format(date_ftmt, MLB_KEY)
    # response = requests.get(games_today_url)
    # data = response.json()
    games = data['league']['games']
    for game in games:
        pprint(game["game"]["id"])
        pprint(game["game"]["scheduled"])


def get_play_by_play(game_id):
    # play_by_play_url = "http://api.sportradar.us/mlb/trial/v6.5/en/games/{}/pbp.json?api_key={}".format(game_id, MLB_KEY)
    # response = requests.get(play_by_play_url)

    data = response.json()
    print(data)
