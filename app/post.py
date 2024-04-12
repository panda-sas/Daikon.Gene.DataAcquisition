import json
import requests
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(filename='post_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# URL to send POST requests to
url = 'http://localhost:8001/api/v2/gene-batch/import-one'

# Path to the JSON file
file_path = '../data/processed/all_genes_uniprot.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Progress bar setup with tqdm
progress = tqdm(total=len(data), desc="Posting Data", unit="item")

# Loop through each item in the JSON array, send a POST request, and update the progress bar
for item in data:
    try:
        response = requests.post(url, json=item)
        if response.status_code == 200:
            progress.update(1)  # Update progress upon successful POST
        else:
            # Log error if the response code is not 200
            logging.error(f'Failed to post item {item}. Status Code: {response.status_code}, Response: {response.text}')
            progress.update(1)
    except requests.exceptions.RequestException as e:
        # Log exceptions like network problems
        logging.error(f'Exception occurred: {e}, Item: {item}')
        progress.update(1)

# Close the progress bar
progress.close()
