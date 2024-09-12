import os
import boto3
import ffmpeg
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

    if os.path.exists(download_path):
        print(f"File already exists at {download_path}. Skipping download.")
    else:
        try:
            s3.download_file(bucket_name, object_key, download_path)
            print(f"Downloaded {object_key} from {bucket_name} to {download_path}")
        except Exception as e:
            raise AirflowException(f"Error downloading file from S3: {str(e)}")

    return download_path

def create_hls_streams(input_file, output_dir):
    # Define the variants for different quality levels
    # Each variant specifies resolution, video bitrate, audio bitrate, max bitrate, and buffer size
    variants = [
        {'resolution': '640x360', 'v_bitrate': '800k', 'a_bitrate': '128k', 'maxrate': '856k', 'bufsize': '1200k', 'output_dir': '360p'},
        {'resolution': '1280x720', 'v_bitrate': '2500k', 'a_bitrate': '128k', 'maxrate': '2678k', 'bufsize': '3750k', 'output_dir': '720p'},
        {'resolution': '1920x1080', 'v_bitrate': '5000k', 'a_bitrate': '128k', 'maxrate': '5350k', 'bufsize': '7500k', 'output_dir': '1080p'}
    ]

    # Ensure the main output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each variant
    for variant in variants:
        # Create a subdirectory for each quality level
        variant_output_dir = os.path.join(output_dir, variant['output_dir'])
        if not os.path.exists(variant_output_dir):
            os.makedirs(variant_output_dir)

        # Define the output file path for the HLS playlist
        output_file = os.path.join(variant_output_dir, 'stream.m3u8')

        # Use ffmpeg to create the HLS stream for this variant
        (
            ffmpeg
            .input(input_file)
            .output(output_file,
                    vf=f"scale={variant['resolution']}", # Set the video resolution
                    vcodec='libx264', # Use H.264 codec for video
                    acodec='aac', # Use AAC codec for audio
                    **{'b:v': variant['v_bitrate'], 'b:a': variant['a_bitrate']}, # Set video and audio bitrates
                    maxrate=variant['maxrate'], # Set maximum bitrate
                    bufsize=variant['bufsize'], # Set buffer size
                    hls_time=2, # Set segment duration to 2 seconds
                    hls_playlist_type='vod', # Set playlist type to Video on Demand
                    hls_segment_filename=os.path.join(variant_output_dir, 'segment%d.ts'), # Set segment filename pattern
                    f='hls') # Set output format to HLS
            .run()
        )
        print(f"Created HLS stream for {variant['resolution']} at {variant_output_dir}")

    # Create the master playlist that references all quality levels
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as master_playlist:
        master_playlist.write('#EXTM3U\n') # Write the M3U8 header
        for variant in variants:
            # Write the stream information for each quality level
            master_playlist.write(f"#EXT-X-STREAM-INF:BANDWIDTH={int(variant['v_bitrate'][:-1]) * 1000},RESOLUTION={variant['resolution']}\n")
            master_playlist.write(f"{variant['output_dir']}/stream.m3u8\n")
    print(f"Created master playlist at {master_playlist_path}")

def process_video(**kwargs):
    # The input_video path is retrieved from the previous task (download_file_from_s3)
    # using Airflow's XCom (cross-communication) feature.
    # XCom allows tasks to exchange small amounts of data.
    # 'ti' stands for TaskInstance, which is automatically provided by Airflow.
    input_video = kwargs['ti'].xcom_pull(task_ids='download_file')

    # input_video is a string containing the full path to the downloaded video file
    # For example: '/tmp/video.mov'

    # Define the output directory where the processed video files will be stored
    output_directory = '/tmp/processed_video'

    # Call the create_hls_streams function to process the video
    # This function will create multiple HLS streams for adaptive bitrate streaming
    create_hls_streams(input_video, output_directory)

    # Return the output directory path
    # This will be stored in XCom and can be used by subsequent tasks (e.g., upload_to_s3)
    return output_directory

def upload_to_s3(**kwargs):
    env_vars = validate_env_vars()
    s3 = boto3.client(
        's3',
        aws_access_key_id=env_vars['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=env_vars['AWS_SECRET_ACCESS_KEY'],
        region_name=env_vars['AWS_DEFAULT_REGION']
    )
    
    bucket_name = env_vars['S3_BUCKET_NAME']
    processed_dir = kwargs['ti'].xcom_pull(task_ids='process_video')

    for root, dirs, files in os.walk(processed_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, processed_dir)
            s3.upload_file(local_path, bucket_name, f"processed/{s3_path}")
            print(f"Uploaded {local_path} to s3://{bucket_name}/processed/{s3_path}")

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='video_processor_dag',
    default_args=default_args,
    description='A DAG that downloads a video from S3, processes it, and uploads the results',
    schedule_interval=None,
) as dag:

    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file_from_s3,
    )

    process_task = PythonOperator(
        task_id='process_video',
        python_callable=process_video,
    )

    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )

    download_task >> process_task >> upload_task
