# -*- coding: utf-8 -*-
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
import datetime
import json
import os

# Set default environment & config
os.environ['MAX_DOWNLOADS'] = os.getenv('MAX_DOWNLOADS', 10)
PROJECT_HOME = '/usr/local/airflow/dags'
OUTPUT_PATH = '/videos'
YOUTUBE_DL_CMD = (
    '/usr/local/bin/youtube-dl -w -i '
    '--max-downloads {{ params.max_downloads }} '
    '--write-info-json "{{ params.playlist_url }}" '
    '-o "{{ params.output }}" || true'
)

# Set up the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime.strptime(
        datetime.datetime.utcnow().date().isoformat(),
        '%Y-%m-%d'
    ) - datetime.timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}
dag = DAG(
    'download_youtube_playlists',
    default_args=default_args,
    schedule_interval=datetime.timedelta(days=1)
)

# Load youtube playlist info
with open(os.path.join(PROJECT_HOME, 'youtube_playlists.json'), 'r') as f:
    playlists = json.loads(f.read())

# Set up DAG components
trigger_task = DummyOperator(
    task_id='trigger',
    dag=dag
)
tasks = []
for playlist in playlists:
    output_folder = os.path.join(OUTPUT_PATH, playlist['name'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    tasks.append(
        BashOperator(
            task_id=playlist['name'],
            bash_command=YOUTUBE_DL_CMD,
            params=dict(
                path=PROJECT_HOME,
                max_downloads=int(os.getenv('MAX_DOWNLOADS')),
                playlist_url=playlist['url'],
                output=os.path.join(output_folder, '%(title)s-%(id)s.%(ext)s'),
            ),
            dag=dag
        )
    )

# Build the DAG
trigger_task >> tasks