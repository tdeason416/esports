from datetime import date, datetime
import airflow
import json
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG

import time
from pprint import pprint
print("HAZEL IS HERE")
print("poop")

args = {
    'owner': 'DABFS',
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

this_run = BashOperator(task_id='get_todays_schedule',
    bash_command="python /home/ec2-user/esports/src/find_daily_events.py", dag=dag)
