import SherwinHack1
import readwrite

# Complete Task + Exit
# -----------------------------

def complete_task(tasks):

    if len(tasks) == 0:
        print("\nNo tasks to complete.")
        return

    SherwinHack1.show_tasks(tasks)

    try:
        task_number = int(
            input("\nComplete Task (enter task number): ")
        )

        if 1 <= task_number <= len(tasks):

            completed_task = tasks.pop(task_number - 1)

            readwrite.update_tasks(tasks)

            print(f"\nCompleted and removed: {completed_task}")

        else:
            print("\nInvalid task number.")

    except ValueError:
        print("\nPlease enter a valid number.")


def exit_program():
    print("\nExiting Task Checklist. Goodbye!")
    return False


