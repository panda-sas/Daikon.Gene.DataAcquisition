import requests
from Bio import SeqIO
import json

def read_fasta_from_url(url):
    response = requests.get(url)
    response.raise_for_status()

    fasta_content = response.text

    # Using StringIO to create a file-like object for SeqIO
    from io import StringIO
    fasta_file = StringIO(fasta_content)

    sequences = {}

    for record in SeqIO.parse(fasta_file, "fasta"):
        # Extracting the Rv number from the identifier
        identifier_parts = record.id.split('|')
        rv_number = identifier_parts[0]
        
        # Using the Rv number as the identifier
        identifier = rv_number
        sequence = str(record.seq)

        # Extracting start and stop values from the description
        description_parts = record.description.split('|')
        start_stop = description_parts[3].split('-')
        start, stop = int(start_stop[0]), int(start_stop[1])

        # Calculating gene length
        gene_length = stop - start + 1

        sequences[identifier] = {
            "Identifier": identifier,
            "Genome Sequence": sequence,
            "Gene Length": gene_length
        }

    return sequences

def write_json(output_data, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

def main():
    fasta_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_genes&file=Mycobacterium_tuberculosis_H37Rv.fasta'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/Downloaded Files-Input/Automated_gene_sequences_with_length.json'

    gene_sequences = read_fasta_from_url(fasta_url)

    output_data = list(gene_sequences.values())

    write_json(output_data, output_file_path)

    print(f"Gene sequences with length saved to {output_file_path}")

if __name__ == "__main__":
    main()
