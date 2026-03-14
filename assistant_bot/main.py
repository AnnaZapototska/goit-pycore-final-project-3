from utils.helper import parse_input, get_command_suggestions, ask_confirmation

from bot import (
    add_birthday_command,
    add_contact_command,
    change_command,
    edit_command,
    change_email_command,
    close_command,
    phone_command,
    search_command,
    birthdays_command,
    add_address_command,
    edit_address_command,
    show_address_command,
    remove_address_command,
    all_command,
    invalid_command,
    hello_command,
    add_note_command,
    show_birthday_command,
    show_notes_command,
    edit_note_command,
    delete_note_command,
    search_notes_command
)

from storage import (
    load_data_contacts, 
    save_data_contacts,
    load_data_notes,
    save_data_notes
)

from utils.colors import AnsiColor, print_colored, input_colored
from tabulate import tabulate
import shutil

def main():
    book = load_data_contacts()
    notes_book = load_data_notes()

    # Show available commands first
    print_colored("Welcome to the assistant bot!")
    # print_colored(
    # "Available commands: "
    # "hello, "
    # "add, "
    # "edit, "
    # "change, "
    # "change-email, "
    # "phone, "
    # "search, "
    # "add-address, "
    # "edit-address, "
    # "show-address, "
    # "remove-address, "
    # "add-birthday <DD.MM.YYYY>, "
    # "show-birthday, "
    # "birthdays, "
    # "all, "
    # "exit / close, "

    # # --- notes commands ---
    # "add_note, "
    # "show_notes, "
    # "edit_note, "
    # "delete_note, "
    # "search_notes <keyword>"
    # )

    while True:
        try:
            user_input = input_colored("assistant> ")
        except KeyboardInterrupt:
            print_colored("\nGood bye!")
            break

        command, args = parse_input(user_input)

        # Prevent executing command when input was empty
        if not command:
            print_colored("Please enter a command.")
            continue

        command_action = COMMANDS.get(command)

        # If command is unknown, suggest the closest valid command
        if command_action is None:
            suggestions = get_command_suggestions(command, COMMANDS.keys(), limit=3)

            if suggestions:
                main_suggestion = suggestions[0]
                print_colored(f"Invalid command. Did you mean: {main_suggestion}?")

                if ask_confirmation():
                    command = main_suggestion
                    command_action = COMMANDS.get(command)
                    print_colored(f"Running: {command}")
                else:
                    other_suggestions = suggestions[1:]
                    if other_suggestions:
                        print_colored("Other suggestions: " + ", ".join(other_suggestions))
                    else:
                        print_colored("No other suggestions found.")
                    print_colored("Please type the command manually.")
                    continue
            else:
                print_colored("Invalid command.")
                continue

        # result = command_action(args, book)
        NOTES_COMMANDS = {"add_note", "show_notes", "edit_note", "delete_note", "search_notes"}
        if command in NOTES_COMMANDS:
            result = command_action(args, notes_book)
        else:
            result = command_action(args, book)

        if ('═' in result):
            print(result) # this is a fancy table already formatted by the command, so just print it as is
        else:
            terminal_width = shutil.get_terminal_size((80, 20)).columns
            print_colored(tabulate([[result]], tablefmt="grid", maxcolwidths=[terminal_width - 10]))

        # Save data after each successful command execution
        save_data_contacts(book)
        save_data_notes(notes_book)

        if command in ["exit", "close"] and not args:
            break


COMMANDS = {
    # --- global commands ---
    "hello": hello_command,
    "all": all_command,
    "search": search_command,
    "exit": close_command,
    "close": close_command,

    # --- contacts commands ---
    "add": add_contact_command,
    "edit": edit_command,
    "change": change_command,
    "change-email": change_email_command,
    "phone": phone_command,
    "add-address": add_address_command,
    "edit-address": edit_address_command,
    "show-address": show_address_command,
    "remove-address": remove_address_command,
    "add-birthday": add_birthday_command,
    "show-birthday": show_birthday_command,
    "birthdays": birthdays_command,

    # --- notes commands ---
    "add_note": add_note_command,
    "show_notes": show_notes_command,
    "edit_note": edit_note_command,
    "delete_note": delete_note_command,
    "search_notes": search_notes_command,
}


if __name__ == "__main__":
    main()

