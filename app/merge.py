import json

def read_json(file_path):
    """Read a JSON file and return the data."""
    with open(file_path, 'r') as file:
        return json.load(file)

def merge_lists(list1, list2):
    """Merge two lists of dictionaries, combining based on shared keys."""
    combined = list1.copy()
    existing_keys = {item['expansionType']: item for item in combined}
    
    for item2 in list2:
        key = item2['expansionType']
        if key in existing_keys:
            # Merge dictionaries for the same expansionType
            combined_value = existing_keys[key]
            combined_value['expansionValue'] = merge_dicts(combined_value['expansionValue'], item2['expansionValue'])
        else:
            combined.append(item2)
    return combined

def merge_dicts(dict1, dict2):
    """Merge two dictionaries based on specific rules."""
    for key, value2 in dict2.items():
        if key in dict1:
            value1 = dict1[key]
            if isinstance(value1, dict) and isinstance(value2, dict):
                dict1[key] = merge_dicts(value1, value2)
            elif isinstance(value1, list) and isinstance(value2, list) and key == 'expansionProps':
                dict1[key] = merge_lists(value1, value2)
            elif value2 is not None:
                dict1[key] = value2
        else:
            dict1[key] = value2
    return dict1

def merge_json_data(file_path1, file_path2):
    """Merge JSON data from two files based on the 'accessionNumber'."""
    data1 = read_json(file_path1)
    data2 = read_json(file_path2)

    merged_data = {}
    # Create a mapping from accessionNumber to data
    for item in data1:
        merged_data[item['accessionNumber']] = item

    for item in data2:
        accession_no = item['accessionNumber']
        if accession_no in merged_data:
            merged_data[accession_no] = merge_dicts(merged_data[accession_no], item)
        else:
            merged_data[accession_no] = item

    # Convert the merged dictionary back to list format
    merged_list = list(merged_data.values())
    return merged_list

def write_json(data, file_path):
    """Write data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Define file paths
file_path1 = '../data/processed/all_genes_uniprot.json'
file_path2 = '../data/processed/all_genes_mycobrowser.json'
output_file_path = '../data/processed/all_genes_merged.json'

# Merge data and write to a new file
merged_data = merge_json_data(file_path1, file_path2)
write_json(merged_data, output_file_path)
