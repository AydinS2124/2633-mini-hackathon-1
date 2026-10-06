import json
from pathlib import Path
from platformdirs import user_data_dir


PROGRAM_NAME = "TaskWare"


# Find the correct data folder for the operating system
data_dir = Path(
    user_data_dir(PROGRAM_NAME)
)


# Create the folder if it does not already exist
data_dir.mkdir(
    parents=True,
    exist_ok=True
)


# File where tasks are stored
data_file_path = data_dir / "tasks.json"


def update_tasks(tasks_dict):
    """
    Save the task dictionary into tasks.json.
    """

    with open(
        data_file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tasks_dict,
            f,
            indent=4
        )

    print(
        f"\nData saved successfully to: "
        f"{data_file_path}"
    )


def load_tasks():
    """
    Load tasks from tasks.json.

    If the file does not exist, return
    an empty dictionary.
    """

    if not data_file_path.exists():
        return {}

    try:

        with open(
            data_file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        print(
            "\nWarning: tasks.json could not be read."
            "\nStarting with an empty task list."
        )

        return {}