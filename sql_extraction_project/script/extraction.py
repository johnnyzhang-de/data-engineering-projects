from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from google.cloud import bigquery


# =========================
# PostgreSQL Configuration
# =========================

DB_USER = "postgres"
DB_PASSWORD = "11111111"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "de_project"

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# =========================
# BigQuery Configuration
# =========================

BQ_PROJECT_ID = "your-gcp-project-id"
BQ_DATASET = "your_dataset"
BQ_TABLE = "raw_customers"

BQ_TABLE_ID = f"{BQ_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"


# =========================
# Create DB Engine
# =========================

def get_postgres_engine():
    engine = create_engine(DB_URL)
    return engine


# =========================
# Get Watermark
# =========================

def get_last_successful_run_time(pipeline_name):
    engine = get_postgres_engine()

    query = """
    select last_successful_run_time
    from etl_watermark
    where pipeline_name = %(pipeline_name)s
    """

    df = pd.read_sql(
        query,
        engine,
        params={"pipeline_name": pipeline_name}
    )

    if df.empty:
        raise ValueError(f"No watermark found for pipeline: {pipeline_name}")

    return df.iloc[0]["last_successful_run_time"]


# =========================
# Extract from PostgreSQL
# =========================

def extract_from_postgres(last_run_time, current_run_time):
    engine = get_postgres_engine()

    query = """
    select *
    from raw_customers
    where updated_at > %(last_run_time)s
      and updated_at <= %(current_run_time)s
    """

    df = pd.read_sql(
        query,
        engine,
        params={
            "last_run_time": last_run_time,
            "current_run_time": current_run_time
        }
    )

    return df


# =========================
# Validate DataFrame
# =========================

def validate_customers_df(df):
    if df.empty:
        print("No new records found.")
        return False

    if "customer_id" not in df.columns:
        raise ValueError("Missing required column: customer_id")

    if "updated_at" not in df.columns:
        raise ValueError("Missing required column: updated_at")

    if df["customer_id"].isnull().any():
        raise ValueError("customer_id contains null values")

    duplicate_count = df.duplicated(subset=["customer_id"]).sum()

    if duplicate_count > 0:
        raise ValueError(f"Found duplicate customer_id records: {duplicate_count}")

    print(f"Validation passed. Row count: {len(df)}")
    return True


# =========================
# Load to BigQuery
# =========================

def load_to_bigquery(df):
    client = bigquery.Client(project=BQ_PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"
    )

    load_job = client.load_table_from_dataframe(
        df,
        BQ_TABLE_ID,
        job_config=job_config
    )

    load_job.result()

    print(f"Loaded {len(df)} rows into BigQuery table: {BQ_TABLE_ID}")


# =========================
# Update Watermark
# =========================

def update_last_successful_run_time(pipeline_name, new_run_time):
    engine = get_postgres_engine()

    query = text("""
    update etl_watermark
    set last_successful_run_time = :new_run_time,
        updated_at = current_timestamp
    where pipeline_name = :pipeline_name
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "new_run_time": new_run_time
            }
        )

    print(f"Watermark updated to: {new_run_time}")


# =========================
# Main Pipeline
# =========================

def run_pipeline():
    pipeline_name = "raw_customers_to_bq"

    try:
        print("Pipeline started.")

        last_run_time = get_last_successful_run_time(pipeline_name)
        current_run_time = datetime.now()

        print(f"Last successful run time: {last_run_time}")
        print(f"Current run time: {current_run_time}")

        df = extract_from_postgres(
            last_run_time=last_run_time,
            current_run_time=current_run_time
        )

        is_valid = validate_customers_df(df)

        if not is_valid:
            print("No data loaded. Watermark will not be updated.")
            return

        load_to_bigquery(df)

        update_last_successful_run_time(
            pipeline_name=pipeline_name,
            new_run_time=current_run_time
        )

        print("Pipeline completed successfully.")

    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()