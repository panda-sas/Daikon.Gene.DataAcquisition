# main.py
import os
from etl.sources.source_uniprot.gene_extractor_uniprot import extract_gene_data
from etl.sources.source_uniprot.data_fetcher_uniprot import fetch_data
from utils.file_operations.write_output_uniprot import save_to_json
from etl.sources.source_uniprot.raw_data_saver import save_raw_data

def main():
    uniprot_url = 'https://rest.uniprot.org/uniprotkb/stream?format=json&query=%28H37Rv%29'
    raw_data_output_file_path = '../data/raw/raw_uniprot_data.json'
    processed_data_output_file_path = '../data/processed/all_genes_uniprot.json'


    try:
        json_data = fetch_data(uniprot_url)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(raw_data_output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_dir = os.path.dirname(processed_data_output_file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
            

        if json_data:
            # Save raw data
            save_raw_data(json_data, raw_data_output_file_path)

            # Extract and save processed data
            genes_data = extract_gene_data(json_data)
            save_to_json(genes_data, processed_data_output_file_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
