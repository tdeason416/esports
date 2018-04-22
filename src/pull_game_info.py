import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import os
import pandas as pd
import numpy as np
import collect_data
from kafka import KafkaProducer

with open('/home/ec2-user/esports/schedule_today.json') as fh:
    games_today = json.load(fh)

for game_id, date in games_today.iteritems():
    if datetime.now() > pd.Timestamp(date):
        game_data = collect_data.get_play_by_play(game_id)
        if game_data['game']['status'] == 'closed':
            games_today.pop(game_id)
        else:
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            producer.send('mlb_games', game_data)

with open('/home/ec2-user/esports/schedule_today.json', 'wb') as fh:
    json.dump(games_today, fh)
        
