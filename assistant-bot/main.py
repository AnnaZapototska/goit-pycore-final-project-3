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
    print(
        "Available commands: hello, add <name> <phone> [email], change <phone_or_email> <new_phone>, "
        "change-email <phone_or_email> <new_email>, phone <phone_or_email>, "
        "add-birthday <phone_or_email> <DD.MM.YYYY>, show-birthday <phone_or_email>, birthdays, all, exit / close"
    )
    print()

    while True:
        user_input = input("Enter a command: ")

        command, args = parse_input(user_input)

        command_action = COMMANDS.get(command, invalid_command)

        result = command_action(args, book)
        print(result)

        if command in ["exit", "close"]:
            save_data(book)  
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
    "exit": close_command,
    "close": close_command,
}

if __name__ == "__main__":
    main()
