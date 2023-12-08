import requests
import csv

def download_file(url, destination):
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)

def read_tab_separated_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        for row in csv_reader:
            data.append(row)
    return data

def main():
    # Replace this URL with the correct one
    file_url = 'https://mycobrowser.epfl.ch/releases/4/get_file?dir=txt&file=Mycobacterium_tuberculosis_H37Rv.txt'
    file_path = '/Users/saswatipanda/workspace/Daikon.Gene.DataAcquisition/POC/Downloaded Files-Input/Mycobacterium_tuberculosis_H37Rv.txt'

    download_file(file_url, file_path)
    
    # Now you can use the read_tab_separated_file function to process the data
    data = read_tab_separated_file(file_path)

    # Example: Print the first few rows
    for row in data[:5]:
        print(row)

if __name__ == "__main__":
    main()
