import json
from pprint import pprint
import requests
from datetime import date, datetime, timedelta
import collect_data
import os

MLB_KEY = os.environ["MLB_KEY"]

collect_data.get_game_schedule()
