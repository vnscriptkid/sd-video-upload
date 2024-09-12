import os
import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException

def validate_env_vars():
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'S3_BUCKET_NAME', 'S3_OBJECT_KEY']
    env_vars = {}
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise AirflowException(f"Missing or empty required environment variable: {var}")
        env_vars[var] = value
    return env_vars

def download_file_from_s3(**kwargs):
    env_vars = validate_env_vars()
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=env_vars['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=env_vars['AWS_SECRET_ACCESS_KEY'],
        region_name=env_vars['AWS_DEFAULT_REGION']
    )
    
    bucket_name = env_vars['S3_BUCKET_NAME']
    object_key = env_vars['S3_OBJECT_KEY']

    download_path = '/tmp/video.mov'

    s3.download_file(bucket_name, object_key, download_path)
    print(f"Downloaded {object_key} from {bucket_name} to {download_path}")

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='s3_download_dag',
    default_args=default_args,
    description='A simple DAG that downloads a file from S3',
    schedule_interval=None,
) as dag:

    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file_from_s3,
    )
