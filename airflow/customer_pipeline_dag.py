from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime

default_args = {
    "owner": "data_engineering",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="customer_sales_pipeline",
    schedule="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    transform_customer_sales = BigQueryInsertJobOperator(
        task_id="transform_customer_sales",
        configuration={
            "query": {
                "query": """
                CREATE OR REPLACE TABLE analytics.customer_sales AS
                SELECT
                    country,
                    SUM(sales) as total_sales
                FROM raw.customer_data
                GROUP BY country
                """,
                "useLegacySql": False,
            }
        },
    )

    transform_customer_sales
