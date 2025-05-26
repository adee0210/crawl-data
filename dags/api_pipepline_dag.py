from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crawlers.multi_thread_crawler import crawl_multi_sources
from src.processors.frame_processor import process_frames


# DAG 1: API pipeline
with DAG(
    dag_id="api_pipeline",
    start_date=datetime(2025, 5, 1),
    schedule="0 0 5,15,25 * *",  # Days 5, 15, 25
    catchup=False,
    description="Pipeline to crawl football videos from API",
    tags=["video_analysis", "api"],
) as api_dag:
    api_crawl_task = PythonOperator(
        task_id="crawl_api",
        python_callable=crawl_multi_sources,
        op_kwargs={"sources": ["api"], "max_frames": 1000},
    )

    api_process_task = PythonOperator(
        task_id="process_frames",
        python_callable=process_frames,
        op_kwargs={"source": "api"},
    )

    api_crawl_task >> api_process_task
