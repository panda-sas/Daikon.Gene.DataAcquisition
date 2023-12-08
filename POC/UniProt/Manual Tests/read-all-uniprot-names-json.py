import json

def extract_protein_names(json_data):
    protein_names = {}
    results = json_data.get('results', [])

    for result in results:
        protein_description = result.get('proteinDescription', {})
        recommended_name = protein_description.get('recommendedName', {})
        full_name = recommended_name.get('fullName', {})
        value = full_name.get('value', None)

        if value:
            protein_accession = result.get('primaryAccession', 'Unknown')
            protein_names[protein_accession] = value

    return protein_names

def main():
    input_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/UniProt/JSON Output/uniprot_data.json'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/UniProt/JSON Output/all_protein_names.json'

    try:
        with open(input_file_path, 'r') as file:
            json_data = json.load(file)

        protein_names = extract_protein_names(json_data)

        with open(output_file_path, 'w') as output_file:
            json.dump(protein_names, output_file, indent=2)

        print(f"Protein names extracted and saved to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
