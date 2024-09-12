from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import ffmpeg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'video_processing',
    default_args=default_args,
    description='A DAG to process videos for adaptive bitrate streaming',
    schedule_interval=timedelta(days=1),
)

def download_video(**kwargs):
    s3 = S3Hook(aws_conn_id='aws_default')
    bucket = os.getenv('S3_RAW_BUCKET')
    key = os.getenv('S3_RAW_KEY')
    local_path = '/tmp/raw_video.mp4'
    s3.get_key(key, bucket_name=bucket).download_file(local_path)
    return local_path

def process_video(**kwargs):
    input_path = kwargs['task_instance'].xcom_pull(task_ids='download_video')
    output_formats = [
        {'resolution': '360p', 'bitrate': '800k'},
        {'resolution': '720p', 'bitrate': '2400k'},
        {'resolution': '1080p', 'bitrate': '4800k'}
    ]
    output_paths = []
    
    for format in output_formats:
        output_path = f"/tmp/processed_{format['resolution']}.mp4"
        (
            ffmpeg
            .input(input_path)
            .output(output_path, vf=f"scale=-1:{format['resolution'][:-1]}", 
                    video_bitrate=format['bitrate'])
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        output_paths.append(output_path)
    
    return output_paths

def upload_processed_videos(**kwargs):
    s3 = S3Hook(aws_conn_id='aws_default')
    bucket = os.getenv('S3_PROCESSED_BUCKET')
    processed_paths = kwargs['task_instance'].xcom_pull(task_ids='process_video')
    
    for path in processed_paths:
        key = f"processed/{os.path.basename(path)}"
        s3.load_file(path, key, bucket_name=bucket)

def cleanup(**kwargs):
    local_paths = [kwargs['task_instance'].xcom_pull(task_ids='download_video')] + \
                  kwargs['task_instance'].xcom_pull(task_ids='process_video')
    for path in local_paths:
        if os.path.exists(path):
            os.remove(path)

download_task = PythonOperator(
    task_id='download_video',
    python_callable=download_video,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_video',
    python_callable=process_video,
    dag=dag,
)

upload_task = PythonOperator(
    task_id='upload_processed_videos',
    python_callable=upload_processed_videos,
    dag=dag,
)

cleanup_task = PythonOperator(
    task_id='cleanup',
    python_callable=cleanup,
    dag=dag,
)

download_task >> process_task >> upload_task >> cleanup_task
