# GCS to BigQuery Ingestion Pipeline

This project demonstrates a simple serverless data ingestion pipeline on Google Cloud.

## Architecture

CSV file
↓
Google Cloud Storage (GCS)
↓
Cloud Function (Python)
↓
BigQuery raw table

## Components

cloud_function_ingest.py  
Python Cloud Function that triggers when a file is uploaded to GCS and loads it into BigQuery.

sample_customer_data.csv  
Example source data file uploaded to GCS.

create_table.sql  
SQL script used to create the BigQuery raw table.

## Technologies Used

- Python
- Google Cloud Functions
- Google Cloud Storage
- BigQuery
