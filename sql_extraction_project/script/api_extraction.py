import time
from datetime import datetime, timezone

import requests
import pandas as pd
from google.cloud import bigquery


# =========================
# Salesforce Configuration
# =========================

SF_INSTANCE_URL = "https://your-domain.my.salesforce.com"
SF_ACCESS_TOKEN = "your_salesforce_access_token"

# Salesforce API version
SF_API_VERSION = "v60.0"


# =========================
# BigQuery Configuration
# =========================

BQ_PROJECT_ID = "your-gcp-project-id"
BQ_DATASET = "raw"
BQ_TABLE = "raw_salesforce_accounts"

BQ_TABLE_ID = f"{BQ_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"


# =========================
# Salesforce SOQL Query
# =========================

def build_salesforce_query(last_run_time):
    """
    Build SOQL query for incremental Salesforce extraction.

    Salesforce datetime format example:
    2026-04-01T00:00:00Z
    """

    last_run_time_str = last_run_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    query = f"""
    SELECT
        Id,
        Name,
        Type,
        Industry,
        Phone,
        Website,
        CreatedDate,
        LastModifiedDate
    FROM Account
    WHERE LastModifiedDate > {last_run_time_str}
    """

    return query


# =========================
# Extract from Salesforce
# =========================

def extract_from_salesforce(query):
    """
    Extract data from Salesforce using REST API and SOQL.
    Handles pagination with nextRecordsUrl.
    """

    base_url = f"{SF_INSTANCE_URL}/services/data/{SF_API_VERSION}/query"

    headers = {
        "Authorization": f"Bearer {SF_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "q": query
    }

    all_records = []
    url = base_url

    while url:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        records = data.get("records", [])
        all_records.extend(records)

        next_records_url = data.get("nextRecordsUrl")

        if next_records_url:
            url = f"{SF_INSTANCE_URL}{next_records_url}"
            params = None
        else:
            url = None

    return all_records


# =========================
# Transform Salesforce Records
# =========================

def transform_salesforce_records(records):
    """
    Convert Salesforce JSON records into a clean pandas DataFrame.
    """

    cleaned_records = []

    for record in records:
        cleaned_records.append({
            "account_id": record.get("Id"),
            "account_name": record.get("Name"),
            "account_type": record.get("Type"),
            "industry": record.get("Industry"),
            "phone": record.get("Phone"),
            "website": record.get("Website"),
            "created_date": record.get("CreatedDate"),
            "last_modified_date": record.get("LastModifiedDate"),
            "etl_loaded_at": datetime.now(timezone.utc)
        })

    df = pd.DataFrame(cleaned_records)

    if df.empty:
        return df

    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df["last_modified_date"] = pd.to_datetime(df["last_modified_date"], errors="coerce")
    df["etl_loaded_at"] = pd.to_datetime(df["etl_loaded_at"], errors="coerce")

    return df


# =========================
# Validate DataFrame
# =========================

def validate_salesforce_accounts_df(df):
    """
    Basic validation before loading to BigQuery.
    """

    if df.empty:
        print("No new records found.")
        return False

    required_columns = [
        "account_id",
        "account_name",
        "created_date",
        "last_modified_date"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if df["account_id"].isnull().any():
        raise ValueError("account_id contains null values")

    duplicate_count = df.duplicated(subset=["account_id"]).sum()

    if duplicate_count > 0:
        raise ValueError(f"Found duplicate account_id records: {duplicate_count}")

    if df["last_modified_date"].isnull().any():
        raise ValueError("last_modified_date contains invalid datetime values")

    print(f"Validation passed. Row count: {len(df)}")

    return True


# =========================
# Load to BigQuery
# =========================

def load_to_bigquery(df):
    """
    Load pandas DataFrame into BigQuery.
    """

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
# Simple Retry Wrapper
# =========================

def extract_with_retry(query, max_retries=3):
    """
    Retry Salesforce extraction if API request fails.
    """

    for attempt in range(max_retries):
        try:
            return extract_from_salesforce(query)

        except requests.exceptions.RequestException as e:
            print(f"Salesforce API request failed. Attempt {attempt + 1}/{max_retries}. Error: {e}")

            if attempt == max_retries - 1:
                raise

            sleep_seconds = 2 ** attempt
            time.sleep(sleep_seconds)


# =========================
# Main Pipeline
# =========================

def run_pipeline():
    """
    Main Salesforce to BigQuery pipeline.
    """

    try:
        print("Salesforce to BigQuery pipeline started.")

        # For practice, hardcode last run time.
        # Later you can replace this with a watermark table.
        last_run_time = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

        query = build_salesforce_query(last_run_time)

        records = extract_with_retry(query)

        df = transform_salesforce_records(records)

        is_valid = validate_salesforce_accounts_df(df)

        if not is_valid:
            print("No data loaded.")
            return

        load_to_bigquery(df)

        print("Salesforce to BigQuery pipeline completed successfully.")

    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()