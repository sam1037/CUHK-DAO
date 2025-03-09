# file for loading data

import os
import json
from pathlib import Path

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

# get a poemObj given its name and issueNumber
def loadOnePoem(poemName, issueNum):
    templatePath = Path(__file__).parent.parent / "data" / f"issueNumber{issueNum}"
    file_to_open = templatePath / f"{poemName}.json"
    with open(file_to_open, 'r', encoding='utf-8') as f:
        poemObj = json.load(f)
    return poemObj