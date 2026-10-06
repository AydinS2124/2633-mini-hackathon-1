import taskfuncs
import readwrite

def main():

    print("\n""#######                      #     #\n"                     
    "   #      ##    ####  #    # #  #  #   ##   #####  ######\n" 
    "   #     #  #  #      #   #  #  #  #  #  #  #    # #\n"      
    "   #    #    #  ####  ####   #  #  # #    # #    # #####\n"  
    "   #    ######      # #  #   #  #  # ###### #####  #\n"     
    "   #    #    # #    # #   #  #  #  # #    # #   #  #\n"      
    "   #    #    #  ####  #    #  ## ##  #    # #    # ######\n")

    start = True
    option = ""
    tasks = {}
    
    while(True):
        if (start):
            option = input("\nWelcome to Taskware. Please pick from the following options:"
           "\nAdd Task"
           "\nComplete Task"
           "\nList Tasks"
           "\nExit\n\n")
            
            tasks = readwrite.load_tasks()
            start = False
        else:
            option = input("\nPlease pick from the following options:"
           "\nAdd Task"
           "\nComplete Task"
           "\nList Tasks"
           "\nExit\n\n")
         
        if (option.strip().lower() == "exit"):
            print("\nExiting Task Checklist. Goodbye!")
            return
        elif(option.strip().lower() == "add task"):
            taskfuncs.add_task(tasks)
            readwrite.update_tasks(tasks)
        elif(option.strip().lower() == "list tasks"):
            taskfuncs.show_tasks(tasks)
        elif (option.strip().lower() == "complete task"):
            taskfuncs.complete_task(tasks)
        else:
            print("Enter a valid input.")
main()
