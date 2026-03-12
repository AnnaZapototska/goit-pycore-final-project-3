from bot import *
from storage import load_data, save_data

def parse_input(user_input: str):
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    book = load_data()

    #show avaiable commands first
    print("Welcome to the assistant bot!")
    print("Available commands: hello, add, change, change-email, phone, add-birthday, show-birthday, birthdays, all, search, exit / close")
    print()

    while True:
        try:
            user_input = input("Enter a command: ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)

        command_action = COMMANDS.get(command, invalid_command)

        result = command_action(args, book)
        print(result)

        save_data(book)

        if command in ["exit", "close"]:
            break


COMMANDS = {
    "hello": hello_command,
    "add": add_contact,
    "change": change_command,
    "change-email": change_email_command,
    "phone": phone_command,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
    "all": all_command,
    "search": search_command,
    "exit": close_command,
    "close": close_command,
}

if __name__ == "__main__":
    main()
