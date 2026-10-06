import readwrite
from datetime import datetime


# Tasks are stored in a dictionary.
# Example:
# {
#     "Chapter 3 problems": {
#         "name": "Chapter 3 problems",
#         "type": "Assignment",
#         "due": "2026-10-10",
#         "urgency": 4,
#         "difficulty": 3
#     }
# }

DATE_FORMAT = "%Y-%m-%d"

TASK_TYPES = ["Lab", "Assignment", "Quiz", "Test"]


def normalize_command(text):
    # Remove spaces and capitals:
    # "Task List" becomes "tasklist"
    return "".join(text.split()).lower()


def format_task(task):
    # Turn a task into one line of text for printing
    due = task["due"] if task["due"] else "no due date"

    return (
        f"[{task['type']}] {task['name']} | due {due} | "
        f"urgency {task['urgency']}/5 | "
        f"difficulty {task['difficulty']}/5"
    )


def is_valid_date(text):
    # Check that the date is real and typed as YYYY-MM-DD
    try:
        datetime.strptime(text, DATE_FORMAT)
        return True

    except ValueError:
        return False


def ask_rating(prompt):
    # Keep asking until the user enters a number from 1 to 5
    while True:

        answer = input(prompt).strip()

        if answer.isdigit():
            number = int(answer)

            if 1 <= number <= 5:
                return number

        print("Please enter a number from 1 to 5.")


def ask_task_type():
    # Keep asking until the user chooses a valid task type
    options = ", ".join(TASK_TYPES)

    while True:

        answer = normalize_command(
            input(f"Task type ({options}): ")
        )

        for task_type in TASK_TYPES:

            if answer == task_type.lower():
                return task_type

        print(f"Please choose one of: {options}.")


def sort_key(task):
    # Sort by:
    # 1. Difficulty - highest first
    # 2. Urgency - highest first
    # 3. Due date - earliest first

    due = task["due"] if task["due"] else "9999-12-31"

    return (
        -task["difficulty"],
        -task["urgency"],
        due
    )


def sorted_tasks(tasks):
    # Return tasks as a sorted list without changing the dictionary
    return sorted(
        tasks.values(),
        key=sort_key
    )


# ------------------------------------------------
# LIST TASKS
# ------------------------------------------------

def show_tasks(tasks):

    if not tasks:
        print("\nNo tasks yet.")
        return

    print("\nTask List (hardest and most urgent first):\n")

    for details in sorted_tasks(tasks):

        due = details["due"] if details["due"] else "none"

        print(
            f"Task: {details['name']:<20} | "
            f"Type: {details['type']:<10} | "
            f"Due: {due:<10} | "
            f"Urgency: {details['urgency']:<2} | "
            f"Difficulty: {details['difficulty']:<2}"
        )


# ------------------------------------------------
# ADD TASK
# ------------------------------------------------

def add_task(tasks):

    # Ask for task name
    name = input(
        "\nAdd Task (enter task name): "
    ).strip()

    # Do not allow blank names
    if name == "":
        print("\nTask name can't be empty.")
        return

    # Check whether task already exists
    if name in tasks:

        overwrite = input(
            f"\n{name} already exists in the task list."
            "\nWould you like to update the task? [Y/N]\n\n"
        )

        if overwrite.strip().lower() == "y":
            print("\nUpdating task...")

        else:

            different_task = input(
                "Would you like to add a different task? [Y/N]\n\n"
            )

            if different_task.strip().lower() == "y":
                add_task(tasks)

            else:
                print("\nLeaving add task operation.")

            return

    # Ask for task type
    task_type = ask_task_type()

    # Ask for due date
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

        print(
            "Invalid date. Use YYYY-MM-DD, "
            "for example 2026-10-10."
        )

    # Ask for urgency and difficulty
    urgency = ask_rating(
        "Urgency (1 = low, 5 = high): "
    )

    difficulty = ask_rating(
        "Difficulty (1 = low, 5 = high): "
    )

    # Create task dictionary
    task = {
        "name": name,
        "type": task_type,
        "due": due,
        "urgency": urgency,
        "difficulty": difficulty
    }

    # Add/update task
    tasks[name] = task

    print(f"\nAdded: {format_task(task)}")

    # Show updated list
    show_tasks(tasks)


# ------------------------------------------------
# COMPLETE TASK
# ------------------------------------------------

def complete_task(tasks):

    if len(tasks) == 0:
        print("\nNo tasks to complete.")
        return

    show_tasks(tasks)

    task_name = input(
        "\nComplete Task (enter task name exactly): "
    ).strip()

    if task_name in tasks:

        completed_task = tasks.pop(task_name)

        # Save updated dictionary
        readwrite.update_tasks(tasks)

        print(
            f"\nCompleted and removed: "
            f"{format_task(completed_task)}"
        )

    else:

        leave = input(
            "\nInvalid task."
            "\nWould you like to exit Complete Task? [Y/N]:\n\n"
        )

        if leave.strip().lower() == "y":
            return

        complete_task(tasks)