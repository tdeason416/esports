from __future__ import print_function
from builtins import range
from datetime import date, datetime
import airflow
import json
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

import time
from pprint import pprint

args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 4, 22, 00)
}

dag = DAG('daily_games', default_args=args, schedule_interval='30 0 * * *')


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

def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)


def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'

run_this = PythonOperator(
    task_id='get_todays_schedule',
    provide_context=True,
    python_callable=get_game_schedule,
    dag=dag)
