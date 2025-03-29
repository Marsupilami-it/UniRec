FROM apache/airflow:2.7.3

COPY poetry.lock pyproject.toml/tmp
RUN pip install poetry && poetry install --no-interaction --no-ansi

COPY orchestration/airflow_dags /opt/airflow/dags

USER airflowop", "-b"