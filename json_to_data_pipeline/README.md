# Customer Orders Data Pipeline

## Overview

This project implements a simple end-to-end data pipeline to process customer and order data from raw JSON files into a clean, structured dataset for analytics.

The pipeline follows a standard ETL (Extract, Transform, Load) design and demonstrates how to handle nested JSON data, apply data cleaning rules, and generate a final dataset.

---

## Tech Stack

* Python
* JSON
* CSV
* Logging

---

## Pipeline Architecture

1. **Extract**

   * Reads raw JSON data from local files
   * Loads data into Python objects

2. **Transform**

   * Flattens nested JSON structures (customer → orders)
   * Filters invalid records (non-completed orders, null amounts)
   * Converts data types (string → float)
   * Removes duplicate records using a set-based approach

3. **Load**

   * Writes cleaned data into a CSV file
   * Output is ready for analytics or downstream processing

---

## Project Structure

```
customer-orders-data-pipeline/
├── main.py
├── data/
│   ├── raw_orders.json
│   └── cleaned_orders.csv
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
```

---

## How to Run

```bash
python main.py
```

---

## Example Output

The pipeline generates a cleaned dataset:

```
customer_id,customer_name,order_id,order_date,amount,status
101,Acme Corp,A1001,2026-03-20T10:30:00,1200.5,completed
102,Beta LLC,B2001,2026-03-19T09:15:00,800.0,completed
```

---

## Key Features

* Handles nested JSON data structures
* Applies business logic filtering during transformation
* Uses logging for pipeline monitoring
* Implements deduplication using efficient set-based logic

---

## Future Improvements

* Add database integration (e.g., BigQuery or PostgreSQL)
* Implement Airflow for scheduling
* Add unit tests and data validation checks
* Support incremental data processing

---
