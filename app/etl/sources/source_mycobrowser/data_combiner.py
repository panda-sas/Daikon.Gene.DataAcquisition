from etl.sources.source_mycobrowser.gene_extractor import extract_gene_info, calculate_gene_length

def combine_data(gene_data, gene_sequences, protein_sequences):
    combined_output = []

    for entry in gene_data:
        gene_id = entry["Locus"]
        gene_info = extract_gene_info(entry)
        gene_sequence_info = gene_sequences.get(gene_id, {"sequence": "", "length": None})
        protein_info = protein_sequences.get(gene_id, {"sequence": "", "length": None})

        combined_info = {
            **gene_info,
            "Genome Sequence": {"Sequence": gene_sequence_info["sequence"]},
            "Protein Sequence": {"Sequence": protein_info["sequence"]},
            "Gene Length": calculate_gene_length(gene_sequence_info["sequence"]),
            "Protein Length": protein_info["length"]
        }

        combined_output.append(combined_info)

    return combined_output
