# Import datetime and date from datetime module and import os.
from datetime import datetime, date
import os

# Create empty dictionary to store usernames and passwords.
user_logins = {}

def get_logins():
    """Stores user details from user.txt into the user_logins dictionary."""

    # Read the user login details from user.txt and store them as a list of strings.
    # For each user login split the string into a list and add the slices as key:value pairs in the dictionary.
    with open("user.txt", "r", encoding="utf-8") as users_file:
        lines = users_file.readlines()
        for line in lines:
            user_details = line.strip("\n").split(", ")
            user_logins[user_details[0]] = user_details[1]


def login():
    """Requests valid user details from user and returns a welcome message."""

    # Loop requesting the username and password from the user.
    while True:
        print("\nPlease note your username and password are case sensitive.")
        global username, password
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # If the user enters details in the dictionary return a welcome message else print an error message.
        if username in user_logins and password == user_logins[username]:
            return f"Welcome {username}"
        elif username in user_logins:
            print("Wrong password, re-enter details.")
        else:
            print("Wrong username, re-enter details.")


def display_menu():
    """Requests an option from the user depending on their username."""

    # Create new menu options depending on if user is 'admin' or not.
    if username == "admin":
        new_menu_options = ["\nds -  Display statistics", "\ngr -  Generate report"]
    else:
        new_menu_options = ["", ""]

    global menu
    menu = input('''\nSelect one of the following options below:
r  -  Registering a user
a  -  Adding a task
va -  View all tasks
vm -  View my task{}{}
e  -  Exit
: '''.format(new_menu_options[1], new_menu_options[0])).lower()


def reg_user():
    """Requests new user details from the admin and updates user.txt and user_logins dictionary."""

    # If user is 'admin' present registration form else print appropriate error message.
    if username == "admin":
        # Loop through requesting a new username and password.
        # If the username does not exist yet and password matches confirmation input write them to user.txt, add them to the dictionary and return a message.
        # Else print appropriate error message.
        while True:
            print("\nPlease note usernames and passwords are case sensitive.")
            new_username = input("Create a username: ")
            new_password = input("Create a password: ")
            password_confirmation = input("Confirm your password: ")
        
            if new_password == password_confirmation and new_username not in user_logins:
                with open("user.txt", "a", encoding="utf-8") as users_file:
                    users_file.write(f"\n{new_username}, {new_password}")
                user_logins[new_username] = new_password
                return "You have successfully registered a new user."

            elif new_password != password_confirmation:
                print("Passwords do not match. Try again.")
            
            else:
                print("This username is taken. Try another username.")
    else:
        return "\nOnly the admin is allowed to register users."


def add_task():
    """Requests task details from user and stores them in tasks.txt."""

    # Request task information frm the user.
    # Loop requesting username to assign the task and break if the username exists.
    while True:  
        user_assigned_task = input("Enter the username of the person to whom the task is assigned: ")
        if user_assigned_task in user_logins:
            break
        print("\nThis username does not exist. Please try again.")
    
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter a description of the task: ")
    task_complete = "No"

    # Use the datetime module to create a date format from the user input and get the current date.
    year = int(input("Enter the year it is due: "))
    month = int(input("Enter the month it is due (as a number): " ))
    day = int(input("Enter the day of the month it is due: "))
    
    date_parts = date(year, month, day)
    due_date = f"{date_parts.strftime('%d')} {date_parts.strftime('%b')} {date_parts.strftime('%Y')}"

    date_assigned = date.today()
    date_assigned = f"{date_assigned.strftime('%d')} {date_assigned.strftime('%b')} {date_assigned.strftime('%Y')}"

    # Write the information for the task into tasks.txt.
    with open("tasks.txt", "a", encoding="utf-8") as tasks_file:
        tasks_file.write(f"\n{user_assigned_task}, {task_title}, {task_description}, {date_assigned}, {due_date}, {task_complete}")


def get_task():
    """Returns a list of tasks from tasks.txt."""

    # Read each task from tasks.txt and store as a list of strings.
    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        lines = tasks_file.readlines()
        task_list = []
        # For each task split the string into a list and add them to task_list.
        for line in lines:
            task_components = line.split(", ")
            task_list.append(task_components)
        return task_list
            
def view_all():
    """Displays all tasks to the user."""

    # Store all the tasks in a variable and called the display_task function for each task.
    task_list = get_task()
    for task in task_list:
        display_task(task)


def view_mine():
    """Displays current user's tasks and presents an edit menu."""

    # Store all the tasks in a variable and use it to make a new list for current user tasks.
    task_list = get_task()
    user_task_list = [task for task in task_list if username == task[0]]

    # For each task in the user_task_list call the display_task function.
    for count, task in enumerate(user_task_list, 1):
        display_task(task, f"Task {count}\n")

    # If the user has tasks assigned to them call edit_menu function else print error message.
    if len(user_task_list) > 0:
        edit_menu(user_task_list)
    else:
        print("\nThere are no tasks assigned to you.")


def edit_menu(tasks):
    """Takes in a list of tasks and requests a task number and an edit option from the user then returns the relevant function."""

    # Loop through requesting a task number from the user.
    while True:
        selection = int(input("\nEnter the task number or '-1' to return to the main menu: "))
        if selection == -1:
            return
        
        elif selection > len(tasks) or selection < 1:
            print("That was not a valid task number. Try again.")
        
        else:
            # Loop through requesting an edit option from the user and call the function corresponding to the option.
            while True:
                option = input("""\nSelect one of the following options below:
mc - Mark task as complete
et - Edit task
: """)
                if option.lower() != "mc" and option.lower() != "et":
                    print("\nThat was not a valid option. Try again.")
                elif option.lower() == "mc":
                    return mark_complete(selection)
                else:
                    return edit_task(selection)


def mark_complete(selection):
    """Takes the number of the selected task and edits completion from 'No' to 'Yes then updates tasks.txt"""

    # Store all the tasks in a variable and use it to make a new list for current user tasks.
    # Get the index of the task from task_list that corresponds with task from user_task_list.
    task_list = get_task()
    user_task_list = [task for task in task_list if username == task[0]]
    line = task_list.index(user_task_list[selection - 1])

    # Reassign the value for that task's completetion from 'No' to 'Yes'.
    task_list[line][5] = "Yes\n"

    # Join the tasks into strings and write them to tasks.txt.
    string_tasks = [", ".join(task) for task in task_list]
    with open("tasks.txt", "w+", encoding="utf-8") as tasks_file:
        for task in string_tasks:
            tasks_file.write(task)


def edit_task(selection):
    """Takes the number of the selected task and edits the part chosen by the user then updates tasks.txt."""

    # Store all the tasks in a variable and use it to make a new list for current user tasks.
    # Get the index of the task from task_list that corresponds with task from user_task_list.
    task_list = get_task()
    user_task_list = [task for task in task_list if username == task[0]]
    line = task_list.index(user_task_list[selection - 1])
    
    # If task is incomplete loop through presenting a menu option else print error message.
    if task_list[line][5].strip("\n") == "No":
        while True:
            option = input("""\nSelect one of the following options below:
cu - Change the username of person to whom the task is assigned
cd - Change the due date of the task
: """)

            if option.lower() != "cu" and option.lower() != "cd":
                print("That was not a valid option. Try again.")
                continue

            # If the user selects change user loop through requesting a valid username.
            elif option.lower() == "cu":
                while True:
                    name = input("Enter the username to whom you want to reassign this task: ")
                    if name not in user_logins:
                        print("That is not a valid username. Try again.")
                    else:
                        # Reassign the username part of the task and update tasks.txt.
                        task_list[line][0] = name
                        string_tasks = [", ".join(task) for task in task_list]

                        with open("tasks.txt", "w+", encoding="utf-8") as tasks_file:
                            for task in string_tasks:
                                tasks_file.write(task)
                        return
            
            # Else if the user selects change due date request a new due date.
            # Reassign the due date part of the task and update tasks.txt.
            else:
                year = int(input("Enter the year it is due: "))
                month = int(input("Enter the month it is due (as a number): " ))
                day = int(input("Enter the day of the month it is due: "))

                date_parts = date(year, month, day)
                due_date = f"{date_parts.strftime('%d')} {date_parts.strftime('%b')} {date_parts.strftime('%Y')}"

                task_list[line][4] = due_date
                string_tasks = [", ".join(task) for task in task_list]

                with open("tasks.txt", "w+", encoding="utf-8") as tasks_file:
                    for task in string_tasks:
                        tasks_file.write(task)
                return
    else:
        print("\nThis task cannot be edited as it has been completed.")
            

def generate_reports():
    """Uses data from tasks.txt and user_logins to create two files called task_overview and user_overview.txt."""

    # Store the tasks in a variable and create variable counters for calculation of report results.
    task_list = get_task()
    
    total_tasks = len(task_list)
    total_users = len(user_logins)

    num_completed_tasks = 0
    num_uncompleted_tasks = 0
    num_overdue_tasks = 0
    
    # Depending on whether the task is incomplete increment the relevant counter variable.
    for task in task_list:
        if task[5].strip("\n") == "No":
            num_uncompleted_tasks += 1
        else:
            num_completed_tasks += 1

        due_date = datetime.strptime(task[4], "%d %b %Y")
        due_date = datetime.date(due_date)

        # If it is overdue increment the overdue counter variable.
        if due_date < date.today():
            num_overdue_tasks += 1

    percentage_incomplete = round(num_uncompleted_tasks / total_tasks * 100)
    percentage_overdue = round(num_overdue_tasks / total_tasks * 100)

    # Write the results to task_overview.txt.
    with open("task_overview.txt", "w", encoding="utf-8") as task_overview_file:
        task_overview_file.write(f"{total_tasks}, {num_completed_tasks}, {num_uncompleted_tasks}, {num_overdue_tasks}, {percentage_incomplete}, {percentage_overdue}\n")

    # Open user_overview.txt in 'w' mode.
    with open("user_overview.txt", "w", encoding="utf-8") as user_overview_file:
        user_overview_file.write(f"{total_users}, {total_tasks}\n")

        # For each user in the dictionary create variable counters for calculation of report results.
        for user in user_logins:
            
            user_total_tasks = 0
            user_uncompleted_tasks = 0
            user_overdue_tasks = 0

            # For each task check if the user is assigned the task and if so do further checks to increment the relevant variable counters.
            for task in task_list:
                if task[0] == user:
                    user_total_tasks += 1

                    if task[5].strip("\n") == "No":
                        user_uncompleted_tasks += 1

                        due_date = datetime.strptime(task[4], "%d %b %Y")
                        due_date = datetime.date(due_date)
                        if due_date < date.today():
                            user_overdue_tasks += 1

            user_completed_tasks = user_total_tasks - user_uncompleted_tasks

            # Use 'and' operator when assigning these variables to avoid ZeroDivisionError in case user is not assigned any tasks.
            user_percentage_tasks = user_total_tasks and round(user_total_tasks / total_tasks * 100)
            user_percentage_completed = user_total_tasks and round(user_completed_tasks / user_total_tasks * 100)
            user_percentage_incompleted = user_total_tasks and round(100 - user_percentage_completed)
            user_percentage_overdue = user_total_tasks and round(user_overdue_tasks / user_total_tasks * 100)

            # Write the overview for the user to the file.
            user_overview_file.write(f"{user}, {user_total_tasks}, {user_percentage_tasks}, {user_percentage_completed}, {user_percentage_incompleted}, {user_percentage_overdue}\n")


def display_task(task_components, task_num = ""):
    """Prints the task components for a task.
    
    Parameters:
    task_components (list): A list of strings representing task components for a specific task.
    task_num (str): A string representation of a number (default is '').
    
    Returns: None
    """

    task = (f"{'-' * 50}\n{task_num}"
            f"{'Task:':25}{task_components[1]}\n"
            f"{'Assigned to:':25}{task_components[0]}\n"
            f"{'Date assigned:':25}{task_components[3]}\n"
            f"{'Due date:':25}{task_components[4]}\n"
            f"{'Task complete?:':25}{task_components[5].strip()}\n"
            "Task description:\n"
            f"{task_components[2]}")
            
    print(task)


def display_reports():
    """Reads the report files and displays the content to the user."""
    
    # Read the contents of task_overview.txt and store it into a variable.
    # Split the contents into a list of strings and display the information to the user.
    with open("task_overview.txt", "r", encoding="utf-8") as task_overview_file:
        line = task_overview_file.read()
        task_overview = line.strip("\n").split(", ")
        
        task_overview = (f"{'-' * 45}\n"
                        f"Task overview:\n"
                        f"{'Total number of tasks:':40}{task_overview[0]}\n"
                        f"{'Total number of completed tasks:':40}{task_overview[1]}\n"
                        f"{'Total number of uncompleted tasks:':40}{task_overview[2]}\n"
                        f"{'Total number of overdue tasks:':40}{task_overview[3]}\n"
                        f"{'Percentage of incomplete tasks:':40}{task_overview[4]} %\n"
                        f"{'Percentage of tasks overdue:':40}{task_overview[5]} %\n"
                        )
        
        print(task_overview)

    # Open user_overview.txt in 'r' mode.
    with open("user_overview.txt", "r", encoding="utf-8") as user_overview_file:
        # Read the first line from user_overview.txt and split the string into a list of strings.
        # Assign each string the relevant variable and display to the user.
        num_of_users, num_of_tasks = user_overview_file.readline().strip("\n").split(", ")
        
        print(f"{'=' * 45}\n"
              f"User overview:\n"
              f"{'Total number of users:':40}{num_of_users}\n"
              f"{'Total number of tasks:':40}{num_of_tasks}\n"
              )

        # Read the remaining lines and store them as a list of strings.
        lines = user_overview_file.readlines()
        
        # For each user_overview split the string into a list and display the overview.
        for line in lines:
            user_overview = line.strip("\n").split(", ")
            user_overview = (f"{'-' * 45}\n"
                             f"{'User:':40}{user_overview[0]}\n"
                             f"{'Number of tasks assigned:':40}{user_overview[1]}\n"
                             f"{'Percentage of tasks assigned:':40}{user_overview[2]} %\n"
                             f"{'Percentage of tasks completed:':40}{user_overview[3]} %\n"
                             f"{'Percentage of tasks uncompleted:':40}{user_overview[4]} %\n"
                             f"{'Percentage of tasks overdue:':40}{user_overview[5]} %\n"
                             )

            print(user_overview)


# Get the logins from user.txt and ask the user for their login details.
print("Welcome to the task manager.")
get_logins()
print(login())

# Loop through presenting the menu and asking the user to select an option.
while True:
    display_menu()

    # Call the function relevant to the users selection.
    if menu == 'r':
        print(reg_user())
            
    elif menu == 'a':
        add_task()
         
    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'ds' and username == "admin":
        # Check if admin selects 'ds' before 'gr' and if so generate reports before displaying them.
        with open("user_overview.txt", "a+", encoding="utf-8") as user_overview_file:
            if os.stat("user_overview.txt").st_size == 0:
                generate_reports()

        display_reports()
        print("Note: You can enter 'gr' to update the report.")
        
    elif menu == "gr" and username == "admin":
        generate_reports()
        print("\nReports have been updated.")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")