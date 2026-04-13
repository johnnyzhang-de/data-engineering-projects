import os
import shutil
import logging
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine


# ========= PostgreSQL connection =========
DB_USER = "postgres"
DB_PASSWORD = "11111111"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "de_project"

DB_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ========= Paths =========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNPROCESSED_DIR = os.path.join(BASE_DIR, "data", "unprocessed")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
FAILED_DIR = os.path.join(BASE_DIR, "data", "failed")


# ========= Logging =========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


FILE_TABLE_MAP = {
    "orders": "raw_orders",
    "customers": "raw_customers",
    "products": "raw_products",
    "vendors": "raw_vendors",
    "shipments": "raw_shipments",
}


def get_engine():
    return create_engine(DB_URL)


def get_target_table(file_name: str):
    lower_name = file_name.lower()
    for prefix, table_name in FILE_TABLE_MAP.items():
        if lower_name.startswith(prefix):
            return table_name
    return None


def load_file_to_raw_table(file_path: str, table_name: str, engine):
    file_name = os.path.basename(file_path)

    logging.info("Reading file: %s", file_name)
    df = pd.read_csv(file_path)

    df["source_file_name"] = file_name
    df["process_datetime"] = datetime.now()

    logging.info("Loaded dataframe shape: %s", df.shape)
    logging.info("Target table: %s", table_name)

    df.to_sql(table_name, engine, if_exists="append", index=False)
    logging.info("Inserted %s rows into %s", len(df), table_name)


def move_file(src_path: str, target_dir: str):
    file_name = os.path.basename(src_path)
    target_path = os.path.join(target_dir, file_name)
    shutil.move(src_path, target_path)
    logging.info("Moved file %s -> %s", file_name, target_dir)


def main():
    logging.info("Starting raw file ingestion...")

    if not os.path.exists(UNPROCESSED_DIR):
        raise FileNotFoundError(f"Unprocessed directory not found: {UNPROCESSED_DIR}")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)

    engine = get_engine()
    files = [f for f in os.listdir(UNPROCESSED_DIR) if f.endswith(".csv")]

    if not files:
        logging.info("No CSV files found in unprocessed folder.")
        return

    for file_name in files:
        file_path = os.path.join(UNPROCESSED_DIR, file_name)
        table_name = get_target_table(file_name)

        if not table_name:
            logging.warning("Skipping unknown file: %s", file_name)
            continue

        try:
            load_file_to_raw_table(file_path, table_name, engine)
            move_file(file_path, PROCESSED_DIR)
        except Exception as e:
            logging.error("Failed to process file %s: %s", file_name, e)
            move_file(file_path, FAILED_DIR)

    logging.info("Raw file ingestion finished.")


if __name__ == "__main__":
    main()