# Module to extract the genes and proteins properties from Uniprot
import logging
from utils.data_formatters.publication_formatter import format_publication


def extract_gene_data(json_data):
    genes_data = []
    results = json_data.get("results", [])

    for result in results:
        uniProtId = result.get("primaryAccession", "")

        genes = result.get("genes", [])
        if genes:
            gene_info = genes[0]
            gene_name = gene_info.get("geneName", {}).get("value", None)
            ordered_locus_names = gene_info.get("orderedLocusNames", [])

            locus_value = None
            for locus in ordered_locus_names:
                locus_value = locus.get("value", None)
                if locus_value:
                    break

            protein_description = result.get("proteinDescription", {})
            recommended_name = protein_description.get("recommendedName", {})
            full_name = recommended_name.get("fullName", {})
            protein_name = full_name.get("value", None)

            # Check if protein name is not available in recommendedName, try submissionNames
            if protein_name is None:
                submission_names = protein_description.get("submissionNames", [])
                for submission_name in submission_names:
                    full_name = submission_name.get("fullName", {})
                    protein_name = full_name.get("value", None)
                    if protein_name:
                        break

            # Expansion Props
            expansion_props = []

            # Catalytic activity

            comments = result.get("comments", [])
            for comment in comments:
                comment_type = comment.get("commentType", "").lower()
                if comment_type == "catalytic activity":
                    reaction = comment.get("reaction", {})
                    activity_name = reaction.get("name", "")
                    activity_ec_number = reaction.get("ecNumber", "")
                    publications = reaction.get("evidences", [])
                    if activity_name:
                        expansion_props.append(
                            {
                                "expansionType": "catalyticActivities",
                                "expansionValue": {
                                    "value": activity_name,
                                    "provenance": activity_ec_number,
                                    "publications": format_publication(publications),
                                    "source": "UniProt",
                                },
                            }
                        )

            # AlphaFold information
            alpha_fold_info = ""

            # Function information
            comments = result.get("comments", [])
            for comment in comments:
                comment_type = comment.get("commentType", "").lower()
                if comment_type == "function":
                    texts = comment.get("texts", [])
                    if texts:
                        for text in texts:
                            value = text.get("value", "")
                            publication = text.get("evidences", [])
                            expansion_props.append(
                                {
                                    "expansionType": "function",
                                    "expansionValue": {
                                        "value": value,
                                        "publications": format_publication(publication),
                                        "source": "UniProt",
                                    },
                                }
                            )
            # Gene Ontology
            uniProtKB_cross_references = result.get("uniProtKBCrossReferences", [])
            for cross_reference in uniProtKB_cross_references:
                if (
                    cross_reference.get("database") == "GO"
                ):  # Check for "database": "GO"
                    # go_id = cross_reference.get('id', '')
                    go_properties = cross_reference.get("properties", [])
                    publications = cross_reference.get("evidences", [])

                    for prop in go_properties:

                        if prop.get("key") == "GoTerm":
                            go_term_value = prop.get("value", "")

                            # If value starts with P: then Gene ontology - Biological Process.
                            # If value starts with F: then Gene ontology - Molecular Function.
                            # If value starts with C: then Gene ontology - Cellular Component.

                            # Remove prefixes "C:", "F:", and "P:" from the values
                            go_term_stripped_value = (
                                go_term_value.lstrip("C:").lstrip("F:").lstrip("P:")
                            )

                            # Determine Gene Ontology category based on properties
                            if go_term_value.startswith("P:"):
                                expansion_props.append(
                                    {
                                        "expansionType": "geneOntologyBiologicalProcess",
                                        "expansionValue": {
                                            "value": go_term_stripped_value,
                                            "publications": format_publication(
                                                publications
                                            ),
                                            "source": "UniProt",
                                        },
                                    }
                                )

                            elif go_term_value.startswith("F:"):
                                expansion_props.append(
                                    {
                                        "expansionType": "geneOntologyMolecularFunction",
                                        "expansionValue": {
                                            "value": go_term_stripped_value,
                                            "publications": format_publication(
                                                publications
                                            ),
                                            "source": "UniProt",
                                        },
                                    }
                                )

                            elif go_term_value.startswith("C:"):
                                expansion_props.append(
                                    {
                                        "expansionType": "geneOntologyCellularComponent",
                                        "expansionValue": {
                                            "value": go_term_stripped_value,
                                            "publications": format_publication(
                                                publications
                                            ),
                                            "source": "UniProt",
                                        },
                                    }
                                )
                elif (
                    cross_reference.get("database") == "AlphaFoldDB"
                ):  # Check for "database": "AlphaFoldDB"
                    alpha_fold_info = cross_reference.get("id", None)

            if locus_value:
                # Some locus values are separated by '/' if they have same value in uniProt, breaking it and duplicating the gene data
                locus_values = locus_value.split("/") if locus_value else [None]
                for single_locus_value in locus_values:
                    gene_data = {
                        "uniProtKB": uniProtId,
                        "strainName": "H37Rv",
                        "accessionNumber": single_locus_value,
                        "proteinNameExpanded": protein_name,
                        "alphaFoldId": alpha_fold_info,  # Assign the whole dictionary
                        "expansionProps": expansion_props,  # Assign the whole list
                        "source": "UniProt",
                    }
                    if gene_name and gene_name.strip():
                        gene_data["name"] = gene_name
                        
                    genes_data.append(gene_data)
                if len(locus_values) > 1:
                    logging.info(
                        f"Created separate gene data entries for split locus value '{single_locus_value}' from '{locus_value}'."
                    )

    return genes_data
