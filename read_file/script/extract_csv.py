# local file read .txt, .log
file_path = 'data-engineering-projects/read_file/data/cleaned_orders.csv'

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())

# open local csv file
import csv
file_path = 'data-engineering-projects/read_file/data/cleaned_orders.csv'
with open(file_path,'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

#open local json
json_path = 'data-engineering-projects/read_file/data/raw_orders.json'
import json
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data)
# open with pandas
import pandas as pd
