import csv
import spacy

# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

# Read the words from the text file
with open('basicwords.txt', 'r') as file:
    words = file.read().splitlines()

# Initialize lists for nouns, verbs, and adjectives
nouns = []
verbs = []
adjectives = []

# Classify each word using SpaCy
for word in words:
    doc = nlp(word)
    pos = doc[0].pos_
    
    if pos == 'NOUN':
        nouns.append(word)
    elif pos == 'VERB':
        verbs.append(word)
    elif pos == 'ADJ':
        adjectives.append(word)

# Write the classified words into a CSV file
with open('basicwords.csv', 'w', newline='') as csvfile:
    fieldnames = ['noun', 'verb', 'adjective']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    max_len = max(len(nouns), len(verbs), len(adjectives))

    for i in range(max_len):
        row = {
            'noun': nouns[i] if i < len(nouns) else '',
            'verb': verbs[i] if i < len(verbs) else '',
            'adjective': adjectives[i] if i < len(adjectives) else ''
        }
        writer.writerow(row)

print("Words classified and written to 'basicwords.csv'")
