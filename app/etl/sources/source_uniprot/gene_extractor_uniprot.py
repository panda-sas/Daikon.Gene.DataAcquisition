# Module to extract the genes and proteins properties from Uniprot
import logging


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

            # Catalytic activity
            catalytic_activities = []
            comments = result.get("comments", [])
            for comment in comments:
                comment_type = comment.get("commentType", "").lower()
                if comment_type == "catalytic activity":
                    reaction = comment.get("reaction", {})
                    activity_name = reaction.get("name", "")
                    activity_ec_number = reaction.get("ecNumber", "")
                    publications = reaction.get("evidences", [])
                    if activity_name:
                        catalytic_activities.append(
                            {
                                "name": activity_name,
                                "ecNumber": activity_ec_number,
                                "publications": publications,
                                "source": "UniProt",
                            }
                        )

            # Gene Ontology
            gene_ontology = {
                "geneOntology": {
                    "cellularComponent": [],
                    "molecularFunction": [],
                    "biologicalProcess": [],
                }
            }

            # AlphaFold information
            alpha_fold_info = {"AlphaFoldDB": {"id": None}}

            # Function information
            function_info = {"Function": []}

            comments = result.get("comments", [])
            for comment in comments:
                comment_type = comment.get("commentType", "").lower()
                if comment_type == "function":
                    texts = comment.get("texts", [])
                    if texts:
                        for text in texts:
                            value = text.get("value", "")
                            publication = text.get("evidences", [])
                            function_info["Function"].append(
                                {"Name": value, "Publications": publication , "source": "UniProt"}
                            )

            uniProtKB_cross_references = result.get("uniProtKBCrossReferences", [])
            for cross_reference in uniProtKB_cross_references:
                if (
                    cross_reference.get("database") == "GO"
                ):  # Check for "database": "GO"
                    # go_id = cross_reference.get('id', '')
                    go_properties = cross_reference.get("properties", [])
                    go_evidence = cross_reference.get("evidences", [])

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
                                gene_ontology["geneOntology"][
                                    "biologicalProcess"
                                ].append(
                                    {
                                        "name": go_term_stripped_value,
                                        "publications": go_evidence,
                                        "source": "UniProt",
                                    }
                                )
                            elif go_term_value.startswith("F:"):
                                gene_ontology["geneOntology"][
                                    "molecularFunction"
                                ].append(
                                    {
                                        "name": go_term_stripped_value,
                                        "publications": go_evidence,
                                        "source": "UniProt",
                                    }
                                )
                            elif go_term_value.startswith("C:"):
                                gene_ontology["geneOntology"][
                                    "cellularComponent"
                                ].append(
                                    {
                                        "name": go_term_stripped_value,
                                        "publications": go_evidence,
                                        "source": "UniProt",
                                    }
                                )

                elif (
                    cross_reference.get("database") == "AlphaFoldDB"
                ):  # Check for "database": "AlphaFoldDB"
                    alpha_fold_info["AlphaFoldDB"]["id"] = cross_reference.get(
                        "id", None
                    )

            if locus_value or gene_name or protein_name:
                # Some locus values are separated by '/' if they have same value in uniProt, breaking it and duplicating the gene data
                locus_values = locus_value.split('/') if locus_value else [None]
                for single_locus_value in locus_values:
                    gene_data = {
                        "uniProtKB": uniProtId,
                        "locus": single_locus_value,
                        "geneName": gene_name,
                        "proteinNameExpanded": protein_name,
                        "catalyticActivities": catalytic_activities,
                        **gene_ontology,
                        **alpha_fold_info,
                        **function_info,
                        "source": "UniProt",
                    }
                    genes_data.append(gene_data)
                if len(locus_values) > 1:
                    logging.info(f"Created separate gene data entries for split locus value '{single_locus_value}' from '{locus_value}'.")
                
    return genes_data
