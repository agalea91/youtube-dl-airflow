# -*- coding: utf-8 -*-
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta
import json
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime.utcnow().date(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'download_youtube_playlists',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)

PROJECT_HOME = '/usr/local/airflow/dags'
OUTPUT_PATH = '/videos'
YOUTUBE_DL_CMD = (
    '/usr/local/bin/youtube-dl -w -i '
    '--max-downloads {{ params.max_downloads }} '
    '--write-info-json {{ params.playlist_url }} '
    '-o {{ params.output }}'
)

# Load youtube playlist info
with open(os.path.join(PROJECT_HOME, 'youtube_playlists.json'), 'r') as f:
    playlists = json.loads(f.read())

# Set up DAG components
for playlist in playlists:
    output_folder = os.path.join(OUTPUT_PATH, playlist['name'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    tasks = [
        BashOperator(
            task_id=playlist['name'],
            bash_command=YOUTUBE_DL_CMD,
            params=dict(
                path=PROJECT_HOME,
                max_downloads=os.getenv('MAX_DOWNLOADS', 10),
                playlist_url=playlist['url'],
                output=os.path.join(output_folder, '%(title)s-%(id)s.%(ext)s'),
            ),
            dag=dag
        )
    ]

trigger_task = TriggerDagRunOperator('download_youtube_playlists')

# Build the DAG
for task in tasks:
    trigger_task >> task