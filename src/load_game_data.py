import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import os
import pandas as pd
import numpy as np
import collect_data
from kafka import KafkaProducer

with open('/home/ec2-user/esports/data/schedule_today.json') as fh:
    games_today = json.load(fh)

new_games_today = games_today.copy()

for game_id, date in games_today.iteritems():
    if datetime.now() > datetime(int(date.split(':')[0].split('-')[0]),
                                 int(date.split(':')[0].split('-')[1]),
                                 int(date.split(':')[0].split('-')[2][:2]),
                                 int(date.split(':')[0].split('T')[1]),
                                 int(date.split(':')[1]),
                                 int(date.split(':')[-1][:2])):
        game_data = collect_data.get_play_by_play(game_id)
        if game_data['game']['status'] == 'closed':
            new_games_today.pop(game_id)
        else:
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            producer.send('mlb_games', game_data)

with open('/home/ec2-user/esports/schedule_today.json', 'w') as fh:
    json.dump(new_games_today, fh)
