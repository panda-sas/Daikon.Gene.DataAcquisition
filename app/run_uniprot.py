# main.py

from etl.sources.source_uniprot.gene_extractor_uniprot import extract_gene_data
from etl.sources.source_uniprot.data_fetcher_uniprot import fetch_data
from utils.file_operations.write_output_uniprot import save_to_json

def main():
    uniprot_url = 'https://rest.uniprot.org/uniprotkb/stream?format=json&query=%28H37Rv%29'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/app/data/processed/all_genes_uniprot.json'

    try:
        json_data = fetch_data(uniprot_url)

        if json_data:
            genes_data = extract_gene_data(json_data)
            save_to_json(genes_data, output_file_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
