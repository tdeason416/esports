from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import collect_data
import os

## Define the DAG object
default_args = {
    'concurrency' : 1,
    'owner': 'DABGFS',
    'email_on_failure': False,
    'depends_on_past': False,
    'start_date': datetime(2018, 4, 21, 00, 00),
    'retries': 5,
    'retry_delay': timedelta(seconds=240),
}
dag = DAG('games_daily', default_args=default_args, schedule_interval='30 0 * * *')

update_games = PythonOperator(
        task_id='load_daily_games',
        python_callable=collect_data.get_game_schedule,
        provide_context=True,
        dag=dag)
