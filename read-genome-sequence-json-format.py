import re
import json

def parse_fasta(fasta_file_path):
    sequences = {}

    with open(fasta_file_path, "r") as fasta_file:
        current_identifier = None
        current_sequence = ""

        for line in fasta_file:
            line = line.strip()

            if line.startswith(">"):
                # New identifier
                if current_identifier is not None:
                    sequences[current_identifier] = current_sequence

                # Extract the identifier from the header
                match = re.match(r">(.+)", line)
                if match:
                    current_identifier = match.group(1).split("|")[0]
                    current_sequence = ""
            else:
                # Sequence line
                current_sequence += line

        # Add the last sequence
        if current_identifier is not None:
            sequences[current_identifier] = current_sequence

    return sequences

def convert_to_json(sequences):
    json_array = []

    for identifier, sequence in sequences.items():
        json_entry = {
            "Identifier": identifier,
            "Genomic Sequence": sequence
        }
        json_array.append(json_entry)

    return json_array

def write_to_file(json_array, output_file_path):
    with open(output_file_path, "w") as output_file:
        json.dump(json_array, output_file, indent=2)

fasta_file_path = "/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files/Mycobacterium_tuberculosis_H37Rv_genes_v4.fasta"  # Replace with the path to your FASTA file
output_file_path = "/Users/saswatipanda/workspace/fun-trials/Card/JSON Files-Output/individual-genome-sequence.json"     # Replace with the desired output file path

sequences = parse_fasta(fasta_file_path)
json_array = convert_to_json(sequences)
write_to_file(json_array, output_file_path)

print(f"Output written to {output_file_path}.")
