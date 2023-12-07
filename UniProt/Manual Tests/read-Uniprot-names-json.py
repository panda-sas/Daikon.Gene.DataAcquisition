import requests
import json

def fetch_uniprot_data(api_url):
    # Make a request to the UniProt API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        print(f"Error fetching UniProt data. Status code: {response.status_code}")
        return None

def save_to_json(data, output_file_path):
    # Save the data to a JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2)

def main():
    # UniProt REST API URL in JSON format
    api_url = 'https://rest.uniprot.org/uniprotkb/stream?format=json&query=%28%28organism_id%3A83332%29%29'

    # Fetch UniProt data
    uniprot_data = fetch_uniprot_data(api_url)

    if uniprot_data:
        # Specify the output file path
        output_file_path = 'uniprot_data.json'

        # Save the UniProt data to a JSON file
        save_to_json(uniprot_data, output_file_path)

        print(f"UniProt data saved to {output_file_path}")

if __name__ == "__main__":
    main()
