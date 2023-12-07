import json
import requests
from io import StringIO
from Bio import SeqIO

def read_fasta_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    fasta_content = response.text

    sequences = {}
    identifier = None
    sequence = ""
    protein_length = None

    for line in fasta_content.splitlines():
        if line.startswith('>'):
            if identifier is not None:
                sequences[identifier] = {"sequence": sequence, "length": protein_length}
            identifier = line.strip()[1:].split('|')[0]
            sequence = ""
            parts = line.strip().split('|')
            if len(parts) >= 4:
                length_part = parts[3].strip()
                if length_part.endswith("AA"):
                    try:
                        protein_length = int(length_part.split()[0])
                    except ValueError:
                        protein_length = None
                else:
                    protein_length = None
            else:
                protein_length = None
        else:
            sequence += line.strip()

    if identifier is not None:
        sequences[identifier] = {"sequence": sequence, "length": protein_length}

    return sequences

def calculate_gene_length(sequence):
    return len(sequence)

fasta_url_genes = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_genes&file=Mycobacterium_tuberculosis_H37Rv.fasta'
fasta_url_proteins = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_proteins&file=Mycobacterium_tuberculosis_H37Rv.fasta'

gene_sequences = read_fasta_from_url(fasta_url_genes)
protein_sequences = read_fasta_from_url(fasta_url_proteins)

combined_output = []

for gene_id, gene_info in gene_sequences.items():
    protein_info = protein_sequences.get(gene_id, {"sequence": "", "length": None})
    combined_output.append({
        "Identifier": gene_id,
        "Genome Sequence": gene_info["sequence"],
        "Protein Sequence": protein_info["sequence"],
        "Gene Length": calculate_gene_length(gene_info["sequence"]),
        "Protein Length": protein_info["length"]
    })

# Save the combined output to a JSON file
output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/Downloaded Files-Input/Automated_gene_protein_sequences_with_length.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_output, output_file, indent=2)

print(f"Combined output saved to {output_file_path}")
