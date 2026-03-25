from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info('pipeline started')
    
    try:
        data = extract_data('data/raw_orders.json')
        logging.info(f"Extract completed. Records: {len(data)}")
        

        transformed = transform_data(data)
        logging.info(f"Transform completed. Records: {len(transformed)}")
        
        load_data(transformed, 'data/cleaned_orders.csv')
        logging.info("Load completed. Output: data/cleaned_orders.csv")
        
    except Exception as e:
        logging.error(f'Pipeline failed:{e}')
    
    else:
        logging.info('Pipeline finished successfully')

if __name__ == "__main__":
    main()