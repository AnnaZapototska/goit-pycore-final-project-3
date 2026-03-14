from utils.helper import parse_input, get_command_suggestions, ask_confirmation
from bot import (
    add_contact_command,
    change_command,
    edit_command,
    edit_phone_command,
    change_email_command,
    delete_contact_command,
    close_command,
    phone_command,
    show_phone_command,
    add_birthday_command,
    search_command,
    show_birthday_command,
    birthdays_command,
    add_address_command,
    edit_address_command,
    show_address_command,
    remove_address_command,
    all_command,
    hello_command,
    help_command,

    # contact groups
    add_group_command,
    all_groups_command,
    delete_group_command,
    add_contact_group_command,
    add_contacts_to_group_command,
    delete_contact_group_command,
    delete_contact_groups_command,
    show_contact_groups_command,
    search_contacts_by_group_command,

    # notes
    add_note_command,
    show_notes_command,
    edit_note_command,
    delete_note_command,
    search_notes_command,
    # tags
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

from utils.colors import print_colored, input_colored, print_as_table
from utils.help_view import build_welcome_message


def main():
    book = load_data_contacts()
    notes_book = load_data_notes()

    print_colored(build_welcome_message())

    while True:
        try:
            user_input = input_colored("assistant> ")
        except KeyboardInterrupt:
            print()  # new line after Ctrl+C
            print_as_table("Good bye!")
            break

        command, args = parse_input(user_input)

        if not command:
            print_colored("Please enter a command.")
            continue

        command_action = COMMANDS.get(command)

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
                        print_colored(
                            "Other suggestions: " + ", ".join(other_suggestions)
                        )
                    else:
                        print_colored("No other suggestions found.")
                    continue
            else:
                print_colored("Invalid command.")
                continue

        notes_commands = {
            "add-note",
            "all-notes",
            "edit-note",
            "delete-note",
            "search-notes",
            "add-note-tag",
            "remove-note-tag",
            "show-notes-tags",
            "search-notes-by-tag",
            "sort-notes-by-tags",
            "all-notes-tags",
        }

        if command in notes_commands:
            result = command_action(args, notes_book)
        else:
            result = command_action(args, book)

        if isinstance(result, str) and "═" in result:
            print(result)
        else:
            print_as_table(result)

        save_data_contacts(book)
        save_data_notes(notes_book)

        if command in ["exit", "close"] and not args:
            break


COMMANDS = {
    # global
    "hello": hello_command,
    "help": help_command,
    "all-contacts": all_command,
    "search-contact": search_command,
    "exit": close_command,
    "close": close_command,
    # contacts
    "add-contact": add_contact_command,
    "edit-contact": edit_command,
    "edit-phone": change_command,
    "edit-email": change_email_command,
    "delete-contact": delete_contact_command,
    "show-primary-phone": phone_command,
    "add-address": add_address_command,
    "edit-address": edit_address_command,
    "show-address": show_address_command,
    "delete-address": remove_address_command,
    "add-birthday": add_birthday_command,
    "show-birthday": show_birthday_command,
    "all-birthdays": birthdays_command,

    # groups
    "add-contact-group": add_contact_group_command,
    "add-contacts-to-group": add_contacts_to_group_command,
    "delete-contact-group": delete_contact_group_command,
    "delete-contact-groups": delete_contact_groups_command,
    "show-contact-groups": show_contact_groups_command,
    "search-contacts-by-group": search_contacts_by_group_command,

    # notes
    "add-note": add_note_command,
    "all-notes": show_notes_command,
    "edit-note": edit_note_command,
    "delete-note": delete_note_command,
    "search-notes": search_notes_command,
    # tags
    "add-note-tag": add_tag_command,
    "remove-note-tag": remove_tag_command,
    "show-notes-tags": show_tags_command,
    "search-notes-by-tag": search_tag_command,
    "sort-notes-by-tags": sort_notes_by_tags_command,
    "all-notes-tags": all_tags_command,
}


if __name__ == "__main__":
    main()
