from Bio import SeqIO

fasta_file_path = "/Users/saswatipanda/workspace/fun-trials/Mycobacterium_tuberculosis_H37Rv_genes_v4.fasta"  
sequences = {}

with open(fasta_file_path, "r") as fasta_file:
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Access sequence ID using record.id and sequence using record.seq
        sequences[record.id] = str(record.seq)

# Now 'sequences' is a dictionary where keys are sequence IDs and values are sequences
print(sequences)
