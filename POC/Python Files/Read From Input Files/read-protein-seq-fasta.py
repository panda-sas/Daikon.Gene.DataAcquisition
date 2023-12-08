import json

def read_fasta_file(file_path):
    sequences = {}
    current_identifier = None
    current_sequence = ""

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                # New identifier
                if current_identifier is not None:
                    sequences[current_identifier] = current_sequence
                current_identifier = line.split('|')[0][1:]
                current_sequence = ""
            else:
                # Sequence line
                current_sequence += line

    # Add the last sequence
    if current_identifier is not None:
        sequences[current_identifier] = current_sequence

    return sequences

# Example usage
fasta_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_proteins_v4.fasta'
protein_sequences = read_fasta_file(fasta_file_path)

# Convert to JSON format
json_output = [{"Identifier": identifier, "Protein Sequence": sequence} for identifier, sequence in protein_sequences.items()]

# Print or save the JSON output
print(json.dumps(json_output, indent=2))


output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Downloaded Files-Input/JSON Files-Output/protein-sequences.json'
with open(output_file_path, 'w') as json_file:
    json.dump(json_output, json_file, indent=2)

print(f"JSON output saved to {output_file_path}")

