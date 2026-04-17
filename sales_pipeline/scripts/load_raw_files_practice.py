import pandas as pd
from sqlalchemy import create_engine
import logging 
import os

def get_engine():

    host = 'localhost'
    port = '5433'
    database = 'de_project'
    user = 'postgres'
    password = '11111111'

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
    return engine

# from sqlalchemy import text
# engine = get_engine()
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT 1"))
#     print(result.scalar())
def extract_csv(file_path:str):
    logging.info(f'starting extracting file {file_path}')

    if not os.path.exists(file_path):
        raise FileNotFoundError (f'file not found {file_path}')
    
    df = pd.read_csv(file_path)

    if df.empty:
        logging.warning(f'{file_path} is empty')
        return None 
    
    logging.info(f'finished extracting file, rows{len(df)}')
    return df
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_folder = os.path.join(base_dir,'data','unprocessed')

def main():
    files = [f for f in os.listdir(file_folder) if f.endswith('.csv')]
    for file in files:
        file_path = os.path.join(file_folder,file)
        df = extract_csv(file_path)
        if df.empty:
            logging.info('%s file is empty',file_path)
        print(df.head())
