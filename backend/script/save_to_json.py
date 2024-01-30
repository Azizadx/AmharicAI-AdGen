import json

def save_json_to_file(data, file_path='prompt_generated/prompts.json'):
    try:
        # Try to read existing data from the file
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
            if isinstance(existing_data, list):
                # If existing data is a list, append new data to it
                existing_data.append(data)
            else:
                # If existing data is not a list, create a list with existing data and append new data
                existing_data = [existing_data, data]
    except FileNotFoundError:
        # If the file doesn't exist, initialize a list with new data
        existing_data = [data]

    # Write the combined data back to the file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)