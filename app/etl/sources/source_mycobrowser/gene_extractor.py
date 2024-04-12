# Gene data extraction and gene length calculation module


def calculate_gene_length(sequence):
    return len(sequence)


def extract_gene_info(entry):
    gene_info = {
        "accessionNumber": entry["Locus"],
        "name": entry["Name"],
        "strainName": "H37Rv",
        "source": "Mycobrowser",
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
            "item1": entry["Start"],
            "item2": entry["Stop"],
            "item3": entry["Strand"],
        },
        "structuralInformation": {
            "pfam": entry["PFAM"],
        },
        "orthologues": [
            {"item1": "M. marinum", "item2": entry["Orthologues M. marinum"]},
            {"item1": "M. smegmatis", "item2": entry["Orthologues M. smegmatis"]},
            {"item1": "M. leprae", "item2": entry["Orthologues M. leprae"]},
            {"item1": "M. bovis", "item2": entry["Orthologues M. bovis"]},
            {"item1": "M. lepromatosis", "item2": entry["Orthologues M. lepromatosis"]},
            {"item1": "M. abscessus", "item2": entry["Orthologues M. abscessus"]},
            {"item1": "M. tuberculosis", "item2": entry["Orthologues M. tuberculosis"]},
            {"item1": "M. haemophilum", "item2": entry["Orthologues M. haemophilum"]},
            {"item1": "M. orygis", "item2": entry["Orthologues M. orygis"]},
        ],
    }
    return gene_info
