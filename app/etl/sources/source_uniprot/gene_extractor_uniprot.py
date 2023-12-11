# Module to extract the genes and proteins data from Uniprot

def extract_gene_data(json_data):
    genes_data = []
    results = json_data.get('results', [])

    for result in results:
        genes = result.get('genes', [])
        if genes:
            gene_info = genes[0]
            gene_name = gene_info.get('geneName', {}).get('value', None)
            ordered_locus_names = gene_info.get('orderedLocusNames', [])

            locus_value = None
            for locus in ordered_locus_names:
                locus_value = locus.get('value', None)
                if locus_value:
                    break

            protein_description = result.get('proteinDescription', {})
            recommended_name = protein_description.get('recommendedName', {})
            full_name = recommended_name.get('fullName', {})
            protein_name = full_name.get('value', None)

            # Check if protein name is not available in recommendedName, try submissionNames
            if protein_name is None:
                submission_names = protein_description.get('submissionNames', [])
                for submission_name in submission_names:
                    full_name = submission_name.get('fullName', {})
                    protein_name = full_name.get('value', None)
                    if protein_name:
                        break

            if locus_value or gene_name or protein_name:
                gene_data = {
                    "Genes": {
                        "Locus": locus_value,
                        "Gene name": gene_name,
                        "Protein name": protein_name
                    }
                }
                genes_data.append(gene_data)

    return genes_data
