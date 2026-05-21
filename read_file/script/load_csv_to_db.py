import psycopg2
import csv

file_path = 'data-engineering-projects/read_file/data/orders_50_row.csv'
batch_size = 10
insert_sql = '''
INSERT INTO orders_50 (
    order_id,
    customer_id,
    order_date,
    product_id,
    quantity,
    unit_price,
    status
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
'''

def connect_database():
    conn = psycopg2.connect(
        database = 'de_project',
        host = 'localhost',
        port = 5433,
        user = 'postgres',
        password = '11111111'
        )
    cursor = conn.cursor()
    return conn, cursor

def load_csv_to_db():
    try:
        conn, cursor = connect_database()
        with open (file_path, 'r', newline = '', encoding= 'utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                record = (
                    row['order_id'],
                    row['customer_id'],
                    row['order_id'],
                    row['total_amount']
                )
                batch.append(record)
                if len(batch) >= batch_size:
                    cursor.executemany(insert_sql,batch)
                    conn.commit()
                    print(f'inserted {len(batch)} rows')
                    batch.clear()
            
        if batch:
            cursor.executemany(insert_sql, batch)
            conn.commit()
            print(f"Inserted {len(batch)} rows")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    load_csv_to_db()

