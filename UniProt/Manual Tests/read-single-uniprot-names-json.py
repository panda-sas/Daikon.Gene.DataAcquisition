import json

def extract_protein_name(json_data):
    try:
        # Navigate through the nested structure to reach the 'value' field
        protein_name = json_data['results'][0]['proteinDescription']['recommendedName']['fullName']['value']
        return protein_name
    except KeyError:
        print("Error: Unable to extract protein name from the JSON data.")
        return None

def main():
    # Assume 'uniprot_data' is the JSON data obtained from the UniProt API
    # You can replace this with the actual JSON data you receive from the API call
    with open('/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/UniProt/JSON Output/uniprot_data.json', 'r') as json_file:
        uniprot_data = json.load(json_file)

    # Extract the protein name
    protein_name = extract_protein_name(uniprot_data)

    if protein_name:
        print(f"Protein Name: {protein_name}")
    else:
        print("Failed to extract protein name.")

if __name__ == "__main__":
    main()
