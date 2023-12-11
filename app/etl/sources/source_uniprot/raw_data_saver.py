import json

def save_raw_data(json_data, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            json.dump(json_data, output_file, indent=2)
        print(f"Raw data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving raw data to {output_file_path}: {e}")