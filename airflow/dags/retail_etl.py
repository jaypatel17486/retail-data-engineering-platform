from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="retail_etl",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    generate = BashOperator(
        task_id="generate_data",
        bash_command="""
        cd /opt/airflow/project &&
        python -m app.generators.generate_all
        """,
    )

    load = BashOperator(
        task_id="load_data",
        bash_command="""
        cd /opt/airflow/project &&
        python -m app.etl.load_all
        """,
    )

    generate >> load