import json
from pathlib import Path
from platformdirs import user_data_dir

PROGRAM_NAME = "TaskWare"

# Find the file path for specific OS
data_dir = Path(user_data_dir(PROGRAM_NAME))

# Make the directory the file path does not already exist
data_dir.mkdir(parents = True, exist_ok = True)

# Define the file path for saved task data
data_file_path = data_dir / "tasks.json"

# Opens (or creates if non-existent) the tasks.json file to write new task data to the file
def update_tasks(tasks_dict):
    with open(data_file_path, 'w', encoding = "utf-8") as f:
        json.dump(tasks_dict, f, indent = 4)
    print(f"Data saved successfully to: {data_file_path}")

# Opens tasks.json file to read and returns the saved data as a dictionary. Returns empty dictionary if there is no saved data
def load_tasks():
    if (not data_file_path.exists()):
        return {}

    with open(data_file_path, 'r', encoding = "utf-8") as f:
        return json.load(f)