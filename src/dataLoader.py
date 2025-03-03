import os
import json

#load the poems, return a list of poem obj representing by dictionaries
def loadAllPoemData():
    # Initialize a list to store poems
    poems = []
    data_folder = 'data'  # Root folder containing the issue folders

    # Recursively walk through the folder structure
    for root, dirs, files in os.walk(data_folder):
        for filename in files:
            # Process only JSON files
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)  # Construct the full file path
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Load the JSON file and append to the poems list
                        poems.append(json.load(f))
                except Exception as e:
                    print(f"Unexpected error with file: {file_path} - {e}")

    return poems