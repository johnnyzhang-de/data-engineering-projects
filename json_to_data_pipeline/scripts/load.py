import csv
def load_data(data, output_path):
    fieldnames = [
    'customer_id',
    'customer_name',
    'order_id',
    'order_date',
    'amount',
    'status'
    ]
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)