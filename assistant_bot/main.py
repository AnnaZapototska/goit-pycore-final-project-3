from utils.helper import parse_input, get_command_suggestions, ask_confirmation

from bot import (
    add_contact,
    change_command,
    edit_command,
    change_email_command,
    delete_contact_command,
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
    hello_command,
    add_note_command,
    show_notes_command,
    edit_note_command,
    delete_note_command,
    search_notes_command,
    add_tag_command,
    remove_tag_command,
    show_tags_command,
    search_tag_command,
    sort_notes_by_tags_command,
    all_tags_command,
)

from storage import (
    load_data_contacts,
    save_data_contacts,
    load_data_notes,
    save_data_notes,
)


def main():
    book = load_data_contacts()
    notes_book = load_data_notes()

    print("Welcome to the assistant bot!")
    print(
        "Available commands: "
        "hello, "
        "add, "
        "edit, "
        "change, "
        "change-email, "
        "delete,"
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
        "exit / close, "
        "add_note, "
        "show_notes, "
        "edit_note, "
        "delete_note, "
        "search_notes <keyword>, "
        "add-tag, "
        "remove-tag, "
        "show-tags, "
        "search-tag, "
        "sort-notes-by-tags, "
        "all-tags"
    )

    while True:
        try:
            user_input = input("Enter a command: ")
        except KeyboardInterrupt:
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)

        if not command:
            print("Please enter a command.")
            continue

        command_action = COMMANDS.get(command)

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

        notes_commands = {
            "add_note",
            "show_notes",
            "edit_note",
            "delete_note",
            "search_notes",
            "add-tag",
            "remove-tag",
            "show-tags",
            "search-tag",
            "sort-notes-by-tags",
            "all-tags",
        }

        if command in notes_commands:
            result = command_action(args, notes_book)
        else:
            result = command_action(args, book)

        print(result)

        save_data_contacts(book)
        save_data_notes(notes_book)

        if command in ["exit", "close"] and not args:
            break


COMMANDS = {
    "hello": hello_command,
    "all": all_command,
    "search": search_command,
    "exit": close_command,
    "close": close_command,

    "add": add_contact,
    "edit": edit_command,
    "change": change_command,
    "change-email": change_email_command,
    "delete": delete_contact_command,
    "phone": phone_command,
    "add-address": add_address_command,
    "edit-address": edit_address_command,
    "show-address": show_address_command,
    "remove-address": remove_address_command,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,

    "add_note": add_note_command,
    "show_notes": show_notes_command,
    "edit_note": edit_note_command,
    "delete_note": delete_note_command,
    "search_notes": search_notes_command,
    "add-tag": add_tag_command,
    "remove-tag": remove_tag_command,
    "show-tags": show_tags_command,
    "search-tag": search_tag_command,
    "sort-notes-by-tags": sort_notes_by_tags_command,
    "all-tags": all_tags_command,
}


if __name__ == "__main__":
    main()