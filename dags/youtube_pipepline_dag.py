from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crawlers.multi_thread_crawler import crawl_multi_sources
from src.processors.frame_processor import process_frames

# DAG 3: YouTube pipeline
with DAG(
    dag_id="youtube_pipeline",
    start_date=datetime(2025, 5, 1),
    schedule="0 0 1,11,21 * *",  # Days 1, 11, 21
    catchup=False,
    description="Pipeline to crawl football videos from YouTube",
    tags=["video_analysis", "youtube"],
) as youtube_dag:
    youtube_crawl_task = PythonOperator(
        task_id="crawl_youtube",
        python_callable=crawl_multi_sources,
        op_kwargs={"sources": ["youtube"], "max_frames": 1000},
    )

    youtube_process_task = PythonOperator(
        task_id="process_frames",
        python_callable=process_frames,
        op_kwargs={"source": "youtube"},
    )

    youtube_crawl_task >> youtube_process_task
