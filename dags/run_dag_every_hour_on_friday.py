from airflow import DAG
from airflow.operators.bash import BashOperator
import os
from dotenv import load_dotenv
from airflow.utils.dates import days_ago
import pendulum
from datetime import datetime

local_tz = pendulum.timezone("Europe/Tallinn")

load_dotenv()
dag_owner = os.getenv('DAG_OWNER', 'default_owner')

args = {
    'owner': dag_owner,
    'retries': 1
}

with DAG(
    dag_id='run_dag_every_hour_on_friday',
    default_args=args,
    description='Run main.py every hour on Fridays',
    schedule_interval='0 * * * 5', 
    start_date=datetime(2024, 9, 11, tzinfo=local_tz),
    catchup=False
) as dag:

    run_script = BashOperator(
        task_id='run_script',
        bash_command='python /opt/airflow/app/main.py'
    )
