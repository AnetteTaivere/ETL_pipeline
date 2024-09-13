from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import datetime

local_tz = pendulum.timezone("Europe/Tallinn")

args = {
    'retries': 1
}


with DAG(
    dag_id='run_dag_every_2_hours',
    default_args=args,
    description='Run main.py every 2 hours (Monday to Thursday, Saturday, Sunday)',
    schedule_interval='0 */2 * * 1-4,6,7', 
    start_date=datetime.now(),
    catchup=False
) as dag:

    run_script = BashOperator(
        task_id='run_script',
        bash_command='python /opt/airflow/app/main.py'
    )