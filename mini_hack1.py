"""
Task Checklist
--------------
Combines:
  - mini_hack1.py    -> banner and main loop
  - SherwinHack1.py  -> add task, show task list, sorting, validation
  - comptsk_exit.py  -> complete task, exit
  - (new)            -> load_tasks / save_tasks, which the other files
                        called but never defined

A task looks like this:
{"name": "Chapter 3 problems", "type": "Assignment",
 "due": "2026-10-10", "urgency": 4, "difficulty": 3}
"""

import json
import os
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"  # dates will look like this: 2026-10-10
TASK_TYPES = ["Lab", "Assignment", "Quiz", "Test"]
SAVE_FILE = "tasks.json"

BANNER = """
#######                      #     #
   #      ##    ####  #    # #  #  #   ##   #####  ######
   #     #  #  #      #   #  #  #  #  #  #  #    # #
   #    #    #  ####  ####   #  #  # #    # #    # #####
   #    ######      # #  #   #  #  # ###### #####  #
   #    #    # #    # #   #  #  #  # #    # #   #  #
   #    #    #  ####  #    #  ## ##  #    # #    # ######
"""


# - Helpers -

def normalize_command(text):
    # Remove spaces and capitals: "Task List" becomes "tasklist"
    return "".join(text.split()).lower()


def format_task(task):
    # Turn a task into one line of text for printing
    due = task["due"] if task["due"] else "no due date"
    return (
        f"[{task['type']}] {task['name']} | due {due} | "
        f"urgency {task['urgency']}/5 | difficulty {task['difficulty']}/5"
    )


def is_valid_date(text):
    # Check the date is real and typed as YYYY-MM-DD
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True
    except ValueError:
        return False


def ask_rating(prompt):
    # Keep asking until we get a number from 1 to 5
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and 1 <= int(answer) <= 5:
            return int(answer)
        print("Please enter a number from 1 to 5.")


def ask_task_type():
    # Keep asking until the user picks Lab, Assignment, Quiz or Test
    options = ", ".join(TASK_TYPES)
    while True:
        answer = normalize_command(input(f"Task type ({options}): "))
        for task_type in TASK_TYPES:
            if answer == task_type.lower():
                return task_type
        print(f"Please choose one of: {options}.")


def sort_key(task):
    # Decides the order: difficulty, then urgency, then due date
    # The minus sign puts the biggest number first
    # No due date counts as far in the future, so it goes last
    due = task["due"] if task["due"] else "9999-12-31"
    return (-task["difficulty"], -task["urgency"], due)


def sort_tasks(tasks):
    # Sort the real list, so task numbers match what is printed
    tasks.sort(key=sort_key)


# - Saving and Loading -

def save_tasks(tasks):
    # Write the whole list to a JSON file
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except OSError as error:
        print(f"\nCould not save tasks: {error}")


def load_tasks():
    # Read the list back in; start empty if there is no (valid) file
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        print(f"\nCould not read {SAVE_FILE}. Starting with an empty list.")
        return []

    required = {"name", "type", "due", "urgency", "difficulty"}
    tasks = [t for t in data if isinstance(t, dict) and required <= t.keys()]
    sort_tasks(tasks)
    return tasks


# - Task List -

def show_tasks(tasks):
    # Nothing to show if the list is empty
    if len(tasks) == 0:
        print("\nNo tasks yet.")
        return

    # Put the most important tasks at the top
    sort_tasks(tasks)

    # Print each task with a number, starting at 1
    print("\nTask List (hardest and most urgent first):")
    for number, task in enumerate(tasks, start=1):
        print(f"  {number}. {format_task(task)}")


# - Add Task -

def add_task(tasks):
    # Ask for the task name
    name = input("\nAdd Task (enter task name): ").strip()

    # Don't allow a blank name
    if name == "":
        print("\nTask name can't be empty.")
        return

    # Ask what kind of task it is
    task_type = ask_task_type()

    # Ask for the due date (optional, Enter skips it)
    due = None
    while True:
        due_input = input(
            "Due date (YYYY-MM-DD), or press Enter to skip: "
        ).strip()

        if due_input == "":
            break
        if is_valid_date(due_input):
            due = due_input
            break
        print("Invalid date. Use YYYY-MM-DD, for example 2026-10-10.")

    # Ask for urgency and difficulty, both 1 to 5
    urgency = ask_rating("Urgency (1 = low, 5 = high): ")
    difficulty = ask_rating("Difficulty (1 = low, 5 = high): ")

    # Build the task and add it to the list
    task = {
        "name": name,
        "type": task_type,
        "due": due,
        "urgency": urgency,
        "difficulty": difficulty,
    }
    tasks.append(task)
    sort_tasks(tasks)

    # Save the list to the file
    save_tasks(tasks)

    print(f"\nAdded: {format_task(task)}")


# - Complete Task + Exit -

def complete_task(tasks):
    if len(tasks) == 0:
        print("\nNo tasks to complete.")
        return

    show_tasks(tasks)

    try:
        task_number = int(input("\nComplete Task (enter task number): "))

        if 1 <= task_number <= len(tasks):
            completed_task = tasks.pop(task_number - 1)
            save_tasks(tasks)
            print(f"\nCompleted and removed: {format_task(completed_task)}")
        else:
            print("\nInvalid task number.")

    except ValueError:
        print("\nPlease enter a valid number.")


def exit_program():
    print("\nExiting Task Checklist. Goodbye!")
    return False


# - Main Menu -

# Each command can be typed as a word or a number
MENU = {
    "1": "tasklist", "tasklist": "tasklist", "list": "tasklist", "show": "tasklist",
    "2": "add", "add": "add", "addtask": "add",
    "3": "complete", "complete": "complete", "done": "complete",
    "completetask": "complete",
    "4": "exit", "exit": "exit", "quit": "exit",
}


def print_menu():
    print("\n--- Menu ---")
    print("  1. Task List")
    print("  2. Add Task")
    print("  3. Complete Task")
    print("  4. Exit")


def main():
    print(BANNER)
    tasks = load_tasks()
    running = True

    while running:
        print_menu()
        choice = MENU.get(normalize_command(input("\nChoose an option: ")))

        if choice == "tasklist":
            show_tasks(tasks)
        elif choice == "add":
            add_task(tasks)
        elif choice == "complete":
            complete_task(tasks)
        elif choice == "exit":
            running = exit_program()
        else:
            print("\nUnknown option. Type 1-4 or a command name.")


if __name__ == "__main__":
    main()