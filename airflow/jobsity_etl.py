from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

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

ingestion = SparkSubmitOperator(
    task_id='jobsity-ingestion',
    application='C:\code\jobsity\src\pipelines\ingestion.py', 
    name='jobsity-ingestion',
    conn_id='spark_default',
    dag=dag,
)

transformation = SparkSubmitOperator(
    task_id='jobsity-transformation',
    application='C:\code\jobsity\src\pipelines\transformation.py', 
    name='jobsity-transformation',
    conn_id='spark_default',
    dag=dag,
)

ingestion >> transformation