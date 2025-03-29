from __future__ import annotations

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.kafka.operators.kafka import KafkaProducerOperator
from airflow.utils.dates import days_ago
from settings import HSOT_KAFKA, PORT_KAFKA
import datetime

KAFKA_TOPIC = "recommendation_data"
SCRAPING_VK = "src/api_adapter/vk_adapter/scrap_vk.py"
SCRAPING_TG = "src/api_adapter/tg_adapter/scrap_tg.py"
PREPROCESSING_VK = "/orchestration/airflow_dags/jobs/scraping_vk_job.py"
PREPROCESSING_TG = "/orchestration/airflow_dags/jobs/scraping_tg_job.py"
TEMP_FILE_VK = "/tmp/vk_data.json"
TEMP_FILE_TG = "/tmp/tg_data.json"

KAFKA_BOOTSTRAP_SERVERS = f"{HSOT_KAFKA}:{PORT_KAFKA}"

with DAG(
    dag_id="data_processing_pipeline",
    schedule_interval=None,
    start_date=days_ago(2),
    catchup=False,
    tags=["recommendation", "data"],
) as dag:
    scrape_data_vk = BashOperator(
        task_id="scrape_data_vk",
        bash_command=f"python {SCRAPING_VK} > {TEMP_FILE_VK}",
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
        check_exist=True
    )

    scrape_data_tg = BashOperator(
        task_id="scrape_data_tg",
        bash_command=f"python {SCRAPING_TG} > {TEMP_FILE_TG}",
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
        check_exist=True
    )

    preprocess_data_vk = BashOperator(
        task_id="preprocess_data_vk",
        bash_command=f"python {PREPROCESSING_VK}",
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
        check_exist=True
    )

    preprocess_data_tg = BashOperator(
        task_id="preprocess_data_tg",
        bash_command=f"python {PREPROCESSING_TG}",
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
        check_exist=True
    )


    send_to_kafka = KafkaProducerOperator(
        task_id="send_to_kafka",
        kafka_topic=KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_from_file=TEMP_FILE_VK,
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
    )

    send_to_kafka_tg = KafkaProducerOperator(
        task_id="send_to_kafka_tg",
        kafka_topic=KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_from_file=TEMP_FILE_TG,
        retries=3,
        retry_delay=datetime.timedelta(minutes=5),
    )

    scrape_data_vk >> preprocess_data_vk >> send_to_kafka
    scrape_data_tg >> preprocess_data_tg >> send_to_kafka_tg
