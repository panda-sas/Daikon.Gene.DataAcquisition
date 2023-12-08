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

gene_sequences = read_fasta('/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_genes_v4.fasta')
protein_sequences = read_fasta('/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_proteins_v4.fasta')

combined_output = []

for gene_id, gene_info in gene_sequences.items():
    protein_info = protein_sequences.get(gene_id, {"sequence": "", "length": None})
    combined_output.append({
        "Identifier": gene_id,
        "Genome Sequence": gene_info["sequence"],
        "Protein Sequence": protein_info["sequence"],
        "Protein Length": protein_info["length"]
    })

# Save the combined output to a JSON file
output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Downloaded Files-Input/JSON Files-Output/test-gene-and-protein-sequences-v1.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_output, output_file, indent=2)

print(f"Combined output saved to {output_file_path}")
