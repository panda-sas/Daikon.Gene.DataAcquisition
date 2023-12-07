import json
import csv
import re

def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            data.append(row)
    return data

def extract_gene_info(entry):
    gene_info = {
        "Gene Summary": {
            "Locus": entry["Locus"],
        },
        "General annotation": {
            "Gene name": entry["Name"],
            "Type": entry["Feature"],
            "Function": entry["Function"],
            "Product": entry["Product"],
            "Functional category": entry["Functional_Category"],
            "Comments": entry["Comments"],
        },
        "Coordinates": {
            "Start": entry["Start"],
            "Stop": entry["Stop"],
            "Orientation": entry["Strand"],
        },
        "Structural Information": {
            "PFAM": entry["PFAM"],
        },
        "Orthologues": {
            "Orthologues M. marinum": entry["Orthologues M. marinum"],
            "Orthologues M. smegmatis": entry["Orthologues M. smegmatis"],
            "Orthologues M. leprae": entry["Orthologues M. leprae"],
            "Orthologues M. bovis": entry["Orthologues M. bovis"],
            "Orthologues M. lepromatosis": entry["Orthologues M. lepromatosis"],
            "Orthologues M. abscessus": entry["Orthologues M. abscessus"],
            "Orthologues M. tuberculosis": entry["Orthologues M. tuberculosis"],
            "Orthologues M. haemophilum": entry["Orthologues M. haemophilum"],
            "Orthologues M. orygis": entry["Orthologues M. orygis"],
        },
    }
    return gene_info

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

def calculate_gene_length(start, stop):
    try:
        start_pos = int(start)
        stop_pos = int(stop)
        gene_length = stop_pos - start_pos + 1
        return gene_length
    except ValueError:
        return None

def calculate_protein_length(header):
    parts = header.split('|')
    
    if len(parts) >= 4:
        length_part = parts[3].strip()

        if length_part.endswith("AA"):
            try:
                protein_length = int(length_part.split()[0])
                return protein_length
            except ValueError:
                return None
    return None


def main():
    csv_file_path = '/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_txt_v4.txt'
    fasta_gene_file_path = '/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_genes_v4.fasta'
    fasta_protein_file_path = '/Users/saswatipanda/workspace/fun-trials/Card/Fasta Files-Input/Mycobacterium_tuberculosis_H37Rv_proteins_v4.fasta'
    output_file_path = '/Users/saswatipanda/workspace/fun-trials/Card/JSON Files-Output/all_combined_output.json'

    gene_data = read_csv(csv_file_path)
    gene_sequences = read_fasta(fasta_gene_file_path)
    protein_sequences = read_fasta(fasta_protein_file_path)

    combined_output = []

    for entry in gene_data:
        gene_id = entry["Locus"]
        gene_sequence = gene_sequences.get(gene_id, "")
        protein_sequence = protein_sequences.get(gene_id, "")

        gene_info = extract_gene_info(entry)
        gene_length = calculate_gene_length(entry["Start"], entry["Stop"])
        protein_length = calculate_protein_length(protein_sequence)


        combined_info = {
            **gene_info,
            "Genome Sequence": {"Sequence": gene_sequence, "Length": gene_length},
            "Protein Sequence": {"Sequence": protein_sequence, "Length": protein_length},
        }

        combined_output.append(combined_info)

    with open(output_file_path, 'w') as json_file:
        json.dump(combined_output, json_file, indent=2)

    print(f"Combined output saved to {output_file_path}")

if __name__ == "__main__":
    main()
