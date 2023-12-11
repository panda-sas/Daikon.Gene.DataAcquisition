# Module for loading data from URLs

import csv
import requests
from io import StringIO


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