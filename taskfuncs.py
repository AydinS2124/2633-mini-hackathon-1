import readwrite

# Add task looks like this:
# {"name": "Chapter 3 problems", 
# "type": "Assignment",
# "due": "2026-10-10", 
# "urgency": 4, 
# "difficulty": 3}

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"  # dates will look like this: 2026-10-10
TASK_TYPES = ["Lab", "Assignment", "Quiz", "Test"]


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

""""
def sort_key(task):
    # Decides the order: difficulty, then urgency, then due date
    # The minus sign puts the biggest number first
    # No due date counts as far in the future, so it goes last
    due = task["due"] if task["due"] else "9999-12-31"
    return (-task["difficulty"], -task["urgency"], due)


def sort_tasks(tasks):
    # Sort the real list, so task numbers match what is printed
    tasks.sort(key=sort_key)
"""

# - Task List -

def show_tasks(tasks):
    # Nothing to show if the list is empty
    if not tasks:
        print("\nNo tasks yet.")
        return
    # Print each task with a number, starting at 1
    print("\nTask List:\n")
    for name, details in tasks.items():
        print(f"Task: {name:<20} | Type: {details.get('type'):<10} | Due: {details.get('due'):<10} | Urgency: {details.get('urgency'):<2} | Difficulty: {details.get('difficulty'):<2}")
"""
    # Put the most important tasks at the top
    sort_tasks(tasks)
"""



# - Add Task -

def add_task(tasks):
    # Ask for the task name
    name = input("\nAdd Task (enter task name): ").strip()

    # Don't allow a blank name
    if name == "":
        print("\nTask name can't be empty.")
        return
    
    # Check if task already exists, determines whether or not to overwrite said task, add a different task, or exit the add task option
    if name in tasks:
            overwrite = input(f"{name} already exists in the task list."
                              "\nWould you like to update the task? [Y/N]\n\n")
            if (overwrite.strip().lower() == 'y'):
                print("\nContinuing...")
            else:
                overwrite = input(f"Would you like to add a different task? [Y/N]\n\n")
                if (overwrite.strip().lower() == 'y'):
                    add_task()
                else:
                    print("Leaving add task operation.")
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
    
    tasks[name] = task

    # Save the list to the text file (Parker's function)
    show_tasks(tasks)

    print(f"\nAdded: {format_task(task)}")
    
def complete_task(tasks):

    if len(tasks) == 0:
        print("\nNo tasks to complete.")
        return

    show_tasks(tasks)
    task = input("\nComplete Task (enter task name exactly): ")

    if task in tasks:
        completed_task = tasks.pop(task)
        readwrite.update_tasks(tasks)
        print(f"\nCompleted and removed: {completed_task}")
    else:
        exit = input("\nInvalid task, would you like to exit complete task? [Y/N]:\n\n")
        
        if(input.strip().lower() == 'y'):
            return
        else:
            complete_task()
