# test_extractor.py
import json

def extract_first_item(raw_data_file_path):
    try:
        with open(raw_data_file_path, 'r') as file:
            json_data = json.load(file)

        if json_data and 'results' in json_data:
            first_item = json_data['results'][0]
            return first_item

    except Exception as e:
        print(f"Error extracting first item: {e}")
    return None

def write_first_item_to_file(first_item, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            json.dump(first_item, output_file, indent=2)
        print(f"First item written to {output_file_path}")

    except Exception as e:
        print(f"Error writing first item to {output_file_path}: {e}")

def main():
    raw_data_file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/app/data/raw/raw_uniprot_data.json'
    output_first_item_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/app/data/raw/extracted_first_item.json'

    try:
        first_item = extract_first_item(raw_data_file_path)

        if first_item:
            print("First item in the raw data:")
            print(json.dumps(first_item, indent=2))

            # Write the first item to a separate file
            write_first_item_to_file(first_item, output_first_item_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
