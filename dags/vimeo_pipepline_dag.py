from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crawlers.multi_thread_crawler import crawl_multi_sources
from src.processors.frame_processor import process_frames

# DAG 2: Vimeo pipeline
with DAG(
    dag_id="vimeo_pipeline",
    start_date=datetime(2025, 5, 1),
    schedule="0 0 3,13,23 * *",  # Days 3, 13, 23
    catchup=False,
    description="Pipeline to crawl football videos from Vimeo",
    tags=["video_analysis", "vimeo"],
) as vimeo_dag:
    vimeo_crawl_task = PythonOperator(
        task_id="crawl_vimeo",
        python_callable=crawl_multi_sources,
        op_kwargs={"sources": ["vimeo"], "max_frames": 1000},
    )

    vimeo_process_task = PythonOperator(
        task_id="process_frames",
        python_callable=process_frames,
        op_kwargs={"source": "vimeo"},
    )

    vimeo_crawl_task >> vimeo_process_task
