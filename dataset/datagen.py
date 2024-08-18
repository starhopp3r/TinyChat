import random
import itertools
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI()
num_data = 1000000
max_workers = 8

basic_words_file = 'basic/basicwords.csv'
sysprompt_file = 'sysprompt.txt'
usrprompt_file = 'usrprompt.txt'
out_file = 'tinychat.txt'

startings = ['greeting', 'question', 'suggestion']
feelings = ['happiness', 'surprise', 'badness', 'fearfulness', 'anger', 'disgust', 'sadness']
endings = ['conclusive', 'reflective', 'open']


def get_prompt():
    # Read system prompt
    try:
        with open(sysprompt_file, 'r') as file:
            sys_prompt = file.readline().strip()
    except FileNotFoundError:
        print(f"The file {sysprompt_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # Read user prompt
    try:
        with open(usrprompt_file, 'r') as file:
            usr_prompt = file.readline().strip()
    except FileNotFoundError:
        print(f"The file {usrprompt_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # Return the system and user prompt
    return sys_prompt, usr_prompt
    

def generate_tinychat_data(system_prompt, user_prompt, noun_choice, verb_choice, adjective_choice):
    # Format user prompt with random choice of parameters
    user_prompt = user_prompt.replace("{starting}", random.choice(startings))
    user_prompt = user_prompt.replace("{feeling}", random.choice(feelings))
    user_prompt = user_prompt.replace("{ending}", random.choice(endings))
    user_prompt = user_prompt.replace("{noun}", noun_choice)
    user_prompt = user_prompt.replace("{verb}", verb_choice)
    user_prompt = user_prompt.replace("{adjective}", adjective_choice)
    # Access the OpenAI GPT-4o mini model with the prompt
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", 
                 "content": system_prompt},
                {"role": "user", 
                 "content": user_prompt}
            ])
        # Extract the generated content
        output_text = completion.choices[0].message.content
        # Open the text file in append mode and write the output
        with open(out_file, "a") as file:
            file.write(output_text + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_training_data():
    # Load the CSV file
    df = pd.read_csv(basic_words_file)
    # Drop rows with NaN values to ensure valid data
    nouns = df['noun'].dropna()
    verbs = df['verb'].dropna()
    adjectives = df['adjective'].dropna()
    # Create all possible combinations of noun, verb, and adjective
    combinations = list(itertools.product(nouns, verbs, adjectives))
    # Shuffle the combinations
    random.shuffle(combinations)
    # Limit to 1,000,000 combinations
    combinations = combinations[:num_data]
    # Get system and user prompts
    system_prompt, user_prompt = get_prompt()
    # Generate data concurrently for all combinations of verb, noun, and adjective
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(generate_tinychat_data, system_prompt, user_prompt, noun, verb, adjective) for noun, verb, adjective in combinations]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Conversation"):
            pass


if __name__ == '__main__':
    generate_training_data()
