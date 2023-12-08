import json

def extract_gene_names(json_data):
    gene_names = {}
    results = json_data.get('results', [])

    for result in results:
        genes = result.get('genes', [])
        if genes:
            ordered_locus_names = genes[0].get('orderedLocusNames', [])
            if ordered_locus_names:
                gene_name = ordered_locus_names[0].get('value', None)
                if gene_name:
                    protein_description = result.get('proteinDescription', {})
                    recommended_name = protein_description.get('recommendedName', {})
                    full_name = recommended_name.get('fullName', {})
                    protein_name = full_name.get('value', None)

                    if protein_name:
                        gene_names[gene_name] = protein_name

    return gene_names

def main():
    input_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/UniProt/JSON Output/uniprot_data.json'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/UniProt/JSON Output/all_gene-protein_names.json'

    try:
        with open(input_file_path, 'r') as file:
            json_data = json.load(file)

        gene_names = extract_gene_names(json_data)

        with open(output_file_path, 'w') as output_file:
            json.dump(gene_names, output_file, indent=2)

        print(f"Gene names extracted and saved to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
