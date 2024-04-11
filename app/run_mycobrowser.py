from etl.sources.source_mycobrowser.data_loader_from_url import read_csv_from_url, read_fasta_from_url
from etl.sources.source_mycobrowser.data_combiner import combine_data
from utils.file_operations.write_output_mycobrowser import write_output
import os

def main():
    csv_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=txt&file=Mycobacterium_tuberculosis_H37Rv.txt'
    fasta_gene_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_genes&file=Mycobacterium_tuberculosis_H37Rv.fasta'
    fasta_protein_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_proteins&file=Mycobacterium_tuberculosis_H37Rv.fasta'
    output_file_path = '../data/processed/all_genes_mycobrowser.json'

    gene_data = read_csv_from_url(csv_url)
    gene_sequences = read_fasta_from_url(fasta_gene_url)
    protein_sequences = read_fasta_from_url(fasta_protein_url)

    combined_output = combine_data(gene_data, gene_sequences, protein_sequences)
    
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    write_output(output_file_path, combined_output)

    print(f"Combined output saved to {output_file_path}")

if __name__ == "__main__":
    main()
