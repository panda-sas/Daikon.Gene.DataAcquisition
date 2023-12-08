import csv
import json

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

def main():
    csv_file_path = '/Users/saswatipanda/workspace/fun-trials/Mycobacterium_tuberculosis_H37Rv_txt_v4.txt'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Downloaded Files-Input/JSON Files-Output/gene_info_output.json'

    gene_data = read_csv(csv_file_path)
    result = []

    for entry in gene_data:
        gene_info = extract_gene_info(entry)
        result.append(gene_info)

    with open(output_file_path, 'w') as json_file:
        json.dump(result, json_file, indent=2)

if __name__ == "__main__":
    main()
