import os
import json
import logging
import time
from datetime import datetime, timedelta
from etl.sources.source_uniprot.gene_extractor_uniprot import extract_gene_data
from etl.sources.source_uniprot.data_fetcher_uniprot import fetch_data
from utils.file_operations.write_output_uniprot import save_to_json
from etl.sources.source_uniprot.raw_data_saver import save_raw_data

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    uniprot_url = 'https://rest.uniprot.org/uniprotkb/stream?format=json&query=%28H37Rv%29'
    raw_data_output_file_path = '../data/raw/raw_uniprot_data.json'
    processed_data_output_file_path = '../data/processed/all_genes_uniprot.json'

    try:
        logging.info("Ensuring output directories exist.")
        output_dirs = [os.path.dirname(raw_data_output_file_path), os.path.dirname(processed_data_output_file_path)]
        for output_dir in output_dirs:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.info(f"Created directory: {output_dir}")

        logging.info("Checking if the raw data file exists and its last modified time.")
        should_fetch = True
        if os.path.exists(raw_data_output_file_path):
            last_modified_time = os.path.getmtime(raw_data_output_file_path)
            if datetime.fromtimestamp(last_modified_time) > datetime.now() - timedelta(hours=24):
                should_fetch = False
                logging.info("Raw data is less than 24 hours old. Skipping fetch.")

        if should_fetch:
            logging.info("Fetching new data from UniProt.")
            json_data = fetch_data(uniprot_url)
            if json_data:
                logging.info("Saving raw data.")
                save_raw_data(json_data, raw_data_output_file_path)
        else:
            logging.info("Loading existing raw data from file.")
            with open(raw_data_output_file_path, 'r') as file:
                json_data = json.load(file)

        logging.info("Extracting gene data.")
        genes_data = extract_gene_data(json_data)

        logging.info("Saving processed gene data.")
        save_to_json(genes_data, processed_data_output_file_path)

    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
