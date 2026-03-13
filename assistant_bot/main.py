from difflib import get_close_matches
from bot import (
    add_contact,
    change_command,
    edit_command,
    change_email_command,
    close_command,
    phone_command,
    add_birthday,
    search_command,
    show_birthday,
    birthdays,
    add_address_command,
    edit_address_command,
    show_address_command,
    remove_address_command,
    all_command,
    invalid_command,
    hello_command
)
from storage import load_data, save_data


def parse_input(user_input: str):
    """
    Parse raw user input into command and arguments.
    Returns an empty command for blank input.
    """
    parts = user_input.strip().split()

    # Handle empty input to avoid IndexError
    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]
    return command, args

def get_command_suggestions(command: str, available_commands, limit=3):
    """
    Return a list of the closest valid commands for mistyped user input.
    First try prefix matching, then fuzzy matching.
    """
    if not command or len(command.strip()) < 2:
        return []

    # Prefix matching for short forms like "sho" -> "show-address"
    prefix_matches = [cmd for cmd in available_commands if cmd.startswith(command)]

    # Fuzzy matching for typos like "sho-address" -> "show-address"
    fuzzy_matches = get_close_matches(command, available_commands, n=limit, cutoff=0.6)

    # Merge results without duplicates while preserving order
    suggestions = []
    for cmd in prefix_matches + fuzzy_matches:
        if cmd not in suggestions:
            suggestions.append(cmd)

    return suggestions[:limit]


def ask_confirmation():
    """
    Ask user for Y/N confirmation.
    Returns True for yes, False for no.
    """
    while True:
        answer = input("Confirm suggestion? (Y/N): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter Y or N.")




def main():
    book = load_data()

    # Show available commands first
    print("Welcome to the assistant bot!")
    print(
        "Available commands: "
        "hello, "
        "add, "
        "edit, "
        "change, "
        "change-email, "
        "phone, "
        "search, "
        "add-address, "
        "edit-address, "
        "show-address, "
        "remove-address, "
        "add-birthday <DD.MM.YYYY>, "
        "show-birthday, "
        "birthdays, "
        "all, "
        "exit / close"
    )

    while True:
        try:
            user_input = input("Enter a command: ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)

        # Prevent executing command when input was empty
        if not command:
            print("Please enter a command.")
            continue

        command_action = COMMANDS.get(command)

        # If command is unknown, suggest the closest valid command
        if command_action is None:
            suggestions = get_command_suggestions(command, COMMANDS.keys(), limit=3)

            if suggestions:
                main_suggestion = suggestions[0]
                print(f"Invalid command. Did you mean: {main_suggestion}?")

                if ask_confirmation():
                    command = main_suggestion
                    command_action = COMMANDS.get(command)
                    print(f"Running: {command}")
                else:
                    other_suggestions = suggestions[1:]
                    if other_suggestions:
                        print("Other suggestions: " + ", ".join(other_suggestions))
                    else:
                        print("No other suggestions found.")
                    print("Please type the command manually.")
                    continue
            else:
                print("Invalid command.")
                continue

        result = command_action(args, book)
        print(result)

        # Save data after each successful command execution
        save_data(book)

        if command in ["exit", "close"] and not args:
            break


COMMANDS = {
    "hello": hello_command,
    "add": add_contact,
    "edit": edit_command,
    "change": change_command,
    "change-email": change_email_command,
    "phone": phone_command,
    "add-address": add_address_command,
    "edit-address": edit_address_command,
    "show-address": show_address_command,
    "remove-address": remove_address_command,
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

