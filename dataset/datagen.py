import random
import itertools
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI()
num_data = 1000000
max_workers = 10

def generate_tinychat_data(verb, noun, adjective):
    try:
        # Access the gpt-4o-mini model with the prompt
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", 
                 "content": "TODO"},
                {"role": "user", 
                 "content": f"TODO"}
            ])
        # Extract the generated content
        output_text = completion.choices[0].message.content
        # Open the text file in append mode and write the output
        with open("tinychat.txt", "a") as file:
            file.write(output_text + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_training_data():
    # Load the CSV file
    df = pd.read_csv('basic/basicwords.csv')
    # Drop rows with NaN values to ensure valid data
    nouns = df['noun'].dropna()
    verbs = df['verb'].dropna()
    adjectives = df['adjective'].dropna()
    # Create all possible combinations of noun, verb, and adjective
    combinations = list(itertools.product(nouns, verbs, adjectives))
    # Shuffle the combinations
    random.shuffle(combinations)
    # Limit to 1,000,000 combinations
    combinations = combinations[:1000000]

    # Generate data concurrently for all combinations of verb, noun, and adjective
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_tinychat_data, verb, noun, adjective) for noun, verb, adjective in combinations]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Conversation"):
            pass

if __name__ == '__main__':
    generate_training_data()
