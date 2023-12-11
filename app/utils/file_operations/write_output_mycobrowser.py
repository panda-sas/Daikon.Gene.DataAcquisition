import json

def write_output(output_file_path, data):
    with open(output_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
