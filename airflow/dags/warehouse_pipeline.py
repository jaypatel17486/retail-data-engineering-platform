from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "jay",
    "depends_on_past": False,
    "retries": 2,
}

with DAG(
    dag_id="warehouse_pipeline",
    description="Retail Warehouse Pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["warehouse"],
) as dag:

    warehouse_refresh = BashOperator(
        task_id="warehouse_refresh",
        bash_command="""
        cd /opt/airflow/project &&
        python -m warehouse.loaders.load_warehouse
        """
    )