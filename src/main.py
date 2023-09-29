import os
from login import login
from signup import signup
from terminal import terminal

def login_menu():
    print("1. Signup")
    print("2. Login")
    print("3. Exit")
    return input("Select an option: ")

def main():
    terminal.banner()
    logged_in_user = None
    while True:
        if logged_in_user is None:
            choice = login_menu()

            menu_actions = {
                '1': signup.signup,
                '2': login.login,
                '3': exit
            }

            selected_action = menu_actions.get(choice)
            if selected_action:
                if selected_action == login.login:
                    logged_in_user = selected_action()
                else:
                    selected_action()
            else:
                print("Invalid choice. Please try again.")
        else:
            os.system('clear')
            terminal.terminal(logged_in_user)

if __name__ == "__main__":
    main()
