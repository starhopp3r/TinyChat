import json

# File names
input_file = 'tinychat.txt'
base_output_file = 'data'

# Parameters
max_entries_per_file = 100000

def create_json_files(input_file, base_output_file, max_entries_per_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    num_files = (total_lines + max_entries_per_file - 1) // max_entries_per_file
    
    for i in range(num_files):
        start_index = i * max_entries_per_file
        end_index = min((i + 1) * max_entries_per_file, total_lines)
        
        data = [{"chat": line.strip()} for line in lines[start_index:end_index]]
        
        output_file = f"{base_output_file}{i+1}.json"
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        
        print(f"{output_file} created with {len(data)} entries.")

# Run the function
create_json_files(input_file, base_output_file, max_entries_per_file)
