# output_handler.py
import json

def save_to_json(data, output_file_path):
    try:
        with open(output_file_path, 'w') as output_file:
            json.dump(data, output_file, indent=2)
        print(f"Data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving data to {output_file_path}: {e}")
