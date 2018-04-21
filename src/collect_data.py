import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import os

MLB_KEY = os.environ["MLB_KEY"]

def get_game_schedule():
    date_frmt = datetime.now().date().strftime('%Y/%m/%d')
    ## Use this for testing
    with open('games_today.json', 'r') as fh:
        data = json.load(fh)
    ## use this for prod
    # data = json.load(open('games_today.json'))
    # games_today_url = "http://api.sportradar.us/mlb/trial/v6.5/en/games/{}/boxscore.json?api_key={}".format(date_ftmt, MLB_KEY)
    # response = requests.get(games_today_url)
    # data = response.dict()
    games = data['league']['games']
    games_today = {}
    for game in games:
        games_today[game["game"]["id"]] = game["game"]["scheduled"]
    with open('../data/schedule_today.json', 'wb') as wf:
        json.dump(games_today, wf)


def get_play_by_play(game_id):
    play_by_play_url = "http://api.sportradar.us/mlb/trial/v6.5/en/games/{}/pbp.json?api_key={}".format(game_id, MLB_KEY)
    response = requests.get(play_by_play_url)
    data = response.json()
    print(data)