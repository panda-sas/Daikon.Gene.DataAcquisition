# Module to extract the genes and proteins data from Uniprot

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

            catalytic_activities = []
            comments = result.get('comments', [])
            for comment in comments:
                comment_type = comment.get('commentType', '').lower()
                if comment_type == 'catalytic activity':
                    reaction = comment.get('reaction', {})
                    activity_name = reaction.get('name', '')
                    if activity_name:
                        catalytic_activities.append(activity_name)

            if locus_value or gene_name or protein_name:
                gene_data = {
                    "Genes": {
                        "Locus": locus_value,
                        "Gene name": gene_name,
                        "Protein name": protein_name,
                        "Catalytic Activity": catalytic_activities
                    }
                }
                genes_data.append(gene_data)

    return genes_data


def save_raw_data(json_data, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            json.dump(json_data, output_file, indent=2)
        print(f"Raw data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving raw data to {output_file_path}: {e}")