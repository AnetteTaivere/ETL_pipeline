from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import datetime

local_tz = pendulum.timezone("Europe/Tallinn")

args = {
    'retries': 1
}


with DAG(
    dag_id='run_dag_every_hour_on_friday',
    default_args=args,
    description='Run main.py every hour on Fridays',
    schedule_interval='0 * * * 5', 
    start_date=datetime.now(),
    catchup=False
) as dag:

    run_script = BashOperator(
        task_id='run_script',
        bash_command='python /opt/airflow/app/main.py'
    )