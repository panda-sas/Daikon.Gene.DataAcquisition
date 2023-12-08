import json

def extract_gene_data(json_data):
    genes_data = []
    results = json_data.get('results', [])

    for result in results:
        genes = result.get('genes', [])
        if genes:
            gene_info = genes[0]
            gene_name = gene_info.get('geneName', {}).get('value', None)
            ordered_locus_names = gene_info.get('orderedLocusNames', [])

            if gene_name and ordered_locus_names:
                locus_value = None
                for locus in ordered_locus_names:
                    locus_value = locus.get('value', None)
                    if locus_value:
                        break

                protein_description = result.get('proteinDescription', {})
                recommended_name = protein_description.get('recommendedName', {})
                full_name = recommended_name.get('fullName', {})
                protein_name = full_name.get('value', None)

                gene_data = {
                    "Genes": {
                        "Locus": locus_value,
                        "Gene name": gene_name,
                        "Protein name": protein_name
                    }
                }
                genes_data.append(gene_data)

    return genes_data

def main():
    input_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/UniProt/JSON Output/uniprot_data.json'
    output_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/UniProt/JSON Output/all_gene_protein_locus.json'

    try:
        with open(input_file_path, 'r') as file:
            json_data = json.load(file)

        genes_data = extract_gene_data(json_data)

        with open(output_file_path, 'w') as output_file:
            json.dump(genes_data, output_file, indent=2)

        print(f"Gene data extracted and saved to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
