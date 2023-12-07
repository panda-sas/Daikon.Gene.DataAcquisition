import requests
from bs4 import BeautifulSoup
import json

def fetch_gene_data(gene_id):
    url = f"https://mycobrowser.epfl.ch/genes/{gene_id}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Gene summary information
        gene_summary = soup.find('div', class_='panel-heading', string='Gene summary information')
        gene_data = {}
        if gene_summary:
            table = gene_summary.find_next('table', class_='general')
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                gene_data[columns[0].text.strip()] = columns[1].text.strip()

        # Protein summary information
        protein_summary = soup.find('div', class_='panel-heading', string='Protein summary information')
        protein_data = {}
        if protein_summary:
            table = protein_summary.find_next('table', class_='general')
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                protein_data[columns[0].text.strip()] = columns[1].text.strip()

        # Structural information
        structural_info = soup.find('div', class_='panel-heading', string='Structural information')
        structural_data = {}
        if structural_info:
            table = structural_info.find_next('table', class_='general')
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                structural_data[columns[0].text.strip()] = columns[1].text.strip()

        # Orthologues
        orthologues_info = soup.find('div', class_='panel-heading', string='Orthologues')
        orthologues_data = []
        if orthologues_info:
            table = orthologues_info.find_next('table', class_='general')
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                columns = row.find_all('td')
                orthologue = {
                    columns[0].text.strip(): columns[1].text.strip(),
                    "Link": columns[1].find('a')['href']
                }
                orthologues_data.append(orthologue)

        # General annotation
        annotation_info = soup.find('div', class_='panel-heading', string='General annotation')
        annotation_data = {}
        if annotation_info:
            table = annotation_info.find_next('table', class_='general')
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                annotation_data[columns[0].text.strip()] = columns[1].text.strip()

        # Coordinates
        coordinates_info = soup.find('div', class_='panel-heading', string='Coordinates')
        coordinates_data = {}
        if coordinates_info:
            table = coordinates_info.find_next('table', class_='general')
            rows = table.find_all('tr')[1:]  # Skip the header row
            columns = rows[0].find_all('td')
            coordinates_data["Type"] = columns[0].text.strip()
            coordinates_data["Start"] = columns[1].text.strip()
            coordinates_data["End"] = columns[2].text.strip()
            coordinates_data["Orientation"] = columns[3].text.strip()

        # Genomic sequence
        genomic_sequence_info = soup.find('div', class_='panel-heading', string='Genomic sequence')
        genomic_sequence_data = {}
        if genomic_sequence_info:
            feature_type = soup.find('select', id='gs_feature_type').find('option', selected=True).text.strip()
            upstream_region = soup.find('input', id='gs_upstream_region')['value'].strip()
            downstream_region = soup.find('input', id='gs_downstream_region')['value'].strip()
            genomic_sequence_data["Feature Type"] = feature_type
            genomic_sequence_data["Upstream Flanking Region (bp)"] = upstream_region
            genomic_sequence_data["Downstream Flanking Region (bp)"] = downstream_region

        # Protein sequence
        protein_sequence_info = soup.find('div', class_='panel-heading', string='Protein sequence')
        protein_sequence_data = {}
        if protein_sequence_info:
            sequence = protein_sequence_info.find_next('pre').text.strip()
            protein_sequence_data["Sequence"] = sequence

        return {
            "Gene Summary": gene_data,
            "Protein Summary": protein_data,
            "Structural Information": structural_data,
            "Orthologues": orthologues_data,
            "General Annotation": annotation_data,
            "Coordinates": coordinates_data,
            "Genomic Sequence": genomic_sequence_data,
            "Protein Sequence": protein_sequence_data
        }

    print(f"Failed to fetch data for gene ID {gene_id}.")
    return None

def write_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    gene_id = "Rv1297"
    gene_data = fetch_gene_data(gene_id)
    if gene_data:
        output_file = "/Users/saswatipanda/workspace/fun-trials/Card/JSON Files-Output/manual-gene_data_output.json"
        write_to_json(gene_data, output_file)
        print(f"Data for gene ID {gene_id} has been written to {output_file}.")

if __name__ == "__main__":
    main()