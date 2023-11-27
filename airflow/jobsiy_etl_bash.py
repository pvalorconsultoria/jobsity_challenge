from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'jobsity_etl',
    default_args=default_args,
    description='A simple DAG to run spark-submit',
    schedule_interval=timedelta(days=1),
)

def spark_submit_string(filepath):
    return f"spark-submit --jars 'C:\jars\mysql-connector-j-8.1.0.jar' {filepath}"

ingestion = BashOperator(
    task_id='jobsity-ingestion',
    bash_command=spark_submit_string('C:/code/jobsity/src/pipelines/ingestion.py'),
    dag=dag,
)

transformation = BashOperator(
    task_id='jobsity-transformation',
    bash_command=spark_submit_string('C:/code/jobsity/src/pipelines/transformation.py'),
    dag=dag,
)

ingestion >> transformation
