import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import os
import pandas as pd
import numpy as np
import collect_data
import pytz
import dateutil.parser
from kafka import KafkaProducer

utc = pytz.UTC

with open('/home/ec2-user/esports/data/schedule_today.json') as fh:
    games_today = json.load(fh)

now = pytz.utc.localize(datetime.utcnow())
for game_id, date in games_today.items():
    if now > dateutil.parser.parse(date):
        try: 
            game_data = collect_data.get_play_by_play(game_id)
        except ValueError:
            games_today.pop(game_id)
            continue
        if game_data['game']['status'] == 'closed':
            games_today.pop(game_id)
        else:
            producer = KafkaProducer(bootstrap_servers='localhost:9092')
            producer.send('mlb_games', str(game_data))

with open('/home/ec2-user/esports/data/schedule_today.json', 'wb') as fh:
    json.dump(games_today, fh)
        
