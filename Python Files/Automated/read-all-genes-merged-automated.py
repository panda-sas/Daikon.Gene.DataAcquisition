import csv
import json
import requests
from io import StringIO
from Bio import SeqIO

def read_csv_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    csv_content = response.text
    csv_file = StringIO(csv_content)
    data = list(csv.DictReader(csv_file, delimiter='\t'))
    return data

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

def main():
    csv_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=txt&file=Mycobacterium_tuberculosis_H37Rv.txt'
    fasta_gene_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_genes&file=Mycobacterium_tuberculosis_H37Rv.fasta'
    fasta_protein_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=fasta_proteins&file=Mycobacterium_tuberculosis_H37Rv.fasta'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/Downloaded Files-Input/Automated_all_genes_info.json'

    gene_data = read_csv_from_url(csv_url)
    gene_sequences = read_fasta_from_url(fasta_gene_url)
    protein_sequences = read_fasta_from_url(fasta_protein_url)

    combined_output = []

    for entry in gene_data:
        gene_id = entry["Locus"]
        gene_info = extract_gene_info(entry)
        gene_sequence_info = gene_sequences.get(gene_id, {"sequence": "", "length": None})
        protein_info = protein_sequences.get(gene_id, {"sequence": "", "length": None})

        combined_info = {
            **gene_info,
            "Genome Sequence": {"Sequence": gene_sequence_info["sequence"]},
            "Protein Sequence": {"Sequence": protein_info["sequence"]},
            "Gene Length": calculate_gene_length(gene_sequence_info["sequence"]),
            "Protein Length": protein_info["length"]
        }

        combined_output.append(combined_info)

    with open(output_file_path, 'w') as json_file:
        json.dump(combined_output, json_file, indent=2)

    print(f"Combined output saved to {output_file_path}")

if __name__ == "__main__":
    main()
