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
    'start_date': datetime(2018, 4, 24, 00)
}

dag = DAG('mongo_consumer', default_args=args, schedule_interval='*/10 * * * *')


this_run = BashOperator(task_id='get_game_data',
    bash_command="python /home/ec2-user/esports/src/kafka_consumer_batch.py", dag=dag)
