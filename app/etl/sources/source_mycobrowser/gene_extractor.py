# Gene data extraction and gene length calculation module

def calculate_gene_length(sequence):
    return len(sequence)


def extract_gene_info(entry):
    gene_info = {
        "Gene Summary": {
            "Locus": entry["Locus"],
        },
        "General annotation": {
            "Gene name": entry["Name"],
            "Type": entry["Feature"],
            "Function": entry["Function"],
            "Product": entry["Product"],
            "Functional category": entry["Functional_Category"],
            "Comments": entry["Comments"],
        },
        "Coordinates": {
            "Start": entry["Start"],
            "Stop": entry["Stop"],
            "Orientation": entry["Strand"],
        },
        "Structural Information": {
            "PFAM": entry["PFAM"],
        },
        "Orthologues": {
            "Orthologues M. marinum": entry["Orthologues M. marinum"],
            "Orthologues M. smegmatis": entry["Orthologues M. smegmatis"],
            "Orthologues M. leprae": entry["Orthologues M. leprae"],
            "Orthologues M. bovis": entry["Orthologues M. bovis"],
            "Orthologues M. lepromatosis": entry["Orthologues M. lepromatosis"],
            "Orthologues M. abscessus": entry["Orthologues M. abscessus"],
            "Orthologues M. tuberculosis": entry["Orthologues M. tuberculosis"],
            "Orthologues M. haemophilum": entry["Orthologues M. haemophilum"],
            "Orthologues M. orygis": entry["Orthologues M. orygis"],
        },
    }
    return gene_info