import json

def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as fasta_file:
        lines = fasta_file.readlines()
        identifier = None
        sequence = ""
        for line in lines:
            if line.startswith('>'):
                if identifier is not None:
                    sequences[identifier] = sequence
                identifier = line.strip()[1:].split('|')[0]
                sequence = ""
            else:
                sequence += line.strip()
        if identifier is not None:
            sequences[identifier] = sequence
    return sequences

gene_sequences = read_fasta('/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_genes_v4.fasta')
protein_sequences = read_fasta('/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_proteins_v4.fasta')

combined_output = []

for gene_id, gene_sequence in gene_sequences.items():
    protein_sequence = protein_sequences.get(gene_id, "")
    combined_output.append({
        "Identifier": gene_id,
        "Genome Sequence": gene_sequence,
        "Protein Sequence": protein_sequence
    })

# Save the combined output to a JSON file
output_file_path = '/Users/saswatipanda/workspace/fun-trials/Card/JSON Files-Output/gene-and-protein-sequences.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_output, output_file, indent=2)

print(f"Combined output saved to {output_file_path}")
