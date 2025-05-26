from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.crawlers.web_crawler import crawl_web
from src.utils.error_handler import handle_error


def web_pipeline_task(**kwargs):
    try:
        crawl_web()
    except Exception as e:
        handle_error(e)


with DAG(
    dag_id="web_pipeline",
    start_date=datetime(2025, 5, 1),
    schedule="0 0 3,13,23 * *",  # Chạy ngày 3, 13, 23 hàng tháng
    catchup=False,
    tags=["video_analysis", "web"],
) as dag:
    web_task = PythonOperator(
        task_id="crawl_web_data",
        python_callable=web_pipeline_task,
    )
