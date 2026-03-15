from google.cloud import bigquery
import logging


def load_to_bigquery(event, context):
    """
    Cloud Function triggered when a file is uploaded to GCS.
    It loads the CSV file into a BigQuery raw table.
    """

    file_name = event["name"]
    bucket_name = event["bucket"]

    logging.info(f"Processing file: {file_name}")

    # only process CSV files
    if not file_name.endswith(".csv"):
        logging.info("Skipping non-csv file")
        return

    client = bigquery.Client()

    table_id = "project_id.raw.customer_data"

    uri = f"gs://{bucket_name}/{file_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    load_job = client.load_table_from_uri(
        uri,
        table_id,
        job_config=job_config
    )

    load_job.result()

    logging.info("File loaded to BigQuery successfully")
