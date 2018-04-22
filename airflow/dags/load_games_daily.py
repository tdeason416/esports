from datetime import date, datetime
import airflow
import json
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from kafka import KafkaProducer

import time
from pprint import pprint

args = {
    'owner': 'DABFS',
    'start_date': datetime(2018, 4, 22, 00)
}

dag = DAG('daily_games', default_args=args, schedule_interval='30 0 * * *')


this_run = BashOperator(task_id='get_todays_schedule',
    bash_command="python /home/ec2-user/esports/src/find_daily_events.py", dag=dag)
