# Gene data extraction and gene length calculation module


def calculate_gene_length(sequence):
    return len(sequence)


def extract_gene_info(entry):
    gene_info = {
        "accessionNumber": entry["Locus"],
        "geneName": entry["Name"],
        "expansionProps": [
            {
                "expansionType": "function",
                "expansionValue": {"value": entry["Function"], "source": "Mycobrowser"},
            }
        ],
        "product": {"value": entry["Product"], "source": "Mycobrowser"},
        "functionalCategory": {
            "value": entry["Functional_Category"],
            "source": "Mycobrowser",
        },
        "comments": {"value": entry["Comments"], "source": "Mycobrowser"},
        "coordinates": {
            "start": entry["Start"],
            "stop": entry["Stop"],
            "orientation": entry["Strand"],
        },
        "structuralInformation": {
            "pfam": entry["PFAM"],
        },
        "orthologues": {
            "M. marinum": entry["Orthologues M. marinum"],
            "M. smegmatis": entry["Orthologues M. smegmatis"],
            "M. leprae": entry["Orthologues M. leprae"],
            "M. bovis": entry["Orthologues M. bovis"],
            "M. lepromatosis": entry["Orthologues M. lepromatosis"],
            "M. abscessus": entry["Orthologues M. abscessus"],
            "M. tuberculosis": entry["Orthologues M. tuberculosis"],
            "M. haemophilum": entry["Orthologues M. haemophilum"],
            "M. orygis": entry["Orthologues M. orygis"],
        },
    }
    return gene_info
