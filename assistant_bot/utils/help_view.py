from tabulate import tabulate
from utils.colors import AnsiColor, table_cell_colored_value

GREEN_FILL = AnsiColor.GREEN.value
GREEN_SHADOW = AnsiColor.BRIGHT_BLACK.value
RESET = AnsiColor.RESET.value
HELP_TEXT_COLOR = AnsiColor.BRIGHT_MAGENTA
HELP_BORDER_COLOR = AnsiColor.BRIGHT_MAGENTA

APP_BANNER = "\n".join(
    [
        f"{GREEN_FILL}█████╗   ██████╗  ███████╗ ██╗   ██╗  ██████╗{RESET}",
        f"{GREEN_FILL}██╔══██╗ ██╔══██╗ ██╔════╝ ██║   ██║ ██╔═══██╗{RESET}",
        f"{GREEN_FILL}██║  ██║ ██████╔╝ █████╗   ██║   ██║ ██║   ██║{RESET}",
        f"{GREEN_FILL}██║  ██║ ██╔══██╗ ██╔══╝   ╚██╗ ██╔╝ ██║   ██║{RESET}",
        f"{GREEN_FILL}█████╔╝  ██║  ██║ ███████╗  ╚████╔╝  ╚██████╔╝{RESET}",
        f"{GREEN_FILL}╚════╝   ╚═╝  ╚═╝ ╚══════╝   ╚═══╝    ╚═════╝{RESET}",
        "",
        "PERSONAL ASSISTANT BOT",
    ]
)

APP_SUBTITLE = "Contacts • Notes"
APP_HINT = f'Type "{GREEN_FILL}help{RESET}" to see all commands'
HELP_GLOBAL_HINT = f'Type "{GREEN_FILL}help-global{RESET}" to see global commands'
HELP_CONTACTS_HINT = f'Type "{GREEN_FILL}help-contacts{RESET}" to see contacts commands'
HELP_NOTES_HINT = f'Type "{GREEN_FILL}help-notes{RESET}" to see notes commands'
HELP_TAGS_HINT = f'Type "{GREEN_FILL}help-tags{RESET}" to see tags commands'

COMMAND_GROUPS = [
    (
        "Global",
        [
            ("hello", "Show a short greeting", "hello"),
            ("help", "Show all available commands", "help"),
            ("help-global", "Show global commands", "help-global"),
            ("help-contacts", "Show contacts commands", "help-contacts"),
            ("help-notes", "Show notes commands", "help-notes"),
            ("help-tags", "Show tags commands", "help-tags"),
            ("all-contacts", "Show all contacts", "all-contacts"),
            ("search-contact", "Search contacts by query", "search-contact John"),
            ("close", "Close the bot", "close"),
            ("exit", "Exit the bot", "exit"),
        ],
    ),
    (
        "Contacts",
        [
            ("add-contact", "Add a new contact", "add-contact John 1234567890 john@mail.com"),
            ("edit-contact", "Edit a contact field by ID", "edit-contact <id> email new@mail.com"),
            ("edit-phone", "Change the primary phone", "edit-phone <id> 0991234567"),
            ("edit-email", "Change the contact email", "edit-email <id> new@mail.com"),
            ("delete-contact", "Delete a contact", "delete-contact <id>"),
            ("show-primary-phone", "Show the primary phone", "show-primary-phone <id>"),
            ("add-address", "Add an address", "add-address <id>"),
            ("edit-address", "Update the address", "edit-address <id>"),
            ("show-address", "Show the address", "show-address <id>"),
            ("delete-address", "Remove the address", "delete-address <id>"),
            ("add-birthday", "Add a birthday", "add-birthday <id> 01.01.2000"),
            ("show-birthday", "Show the birthday", "show-birthday <id>"),
            ("all-birthdays", "Show upcoming birthdays", "all-birthdays"),
        ],
    ),
    (
        "Notes",
        [
            ("add-note", "Create a new note", "add-note"),
            ("all-notes", "Show all notes", "all-notes"),
            ("edit-note", "Edit a note", "edit-note <id>"),
            ("delete-note", "Delete a note", "delete-note <id>"),
            ("search-notes", "Search notes", "search-notes report"),
        ],
    ),
    (
        "Tags",
        [
            ("add-note-tag", "Add a tag to a note", "add-note-tag <note_id> work"),
            ("remove-note-tag", "Remove a tag from a note", "remove-note-tag <note_id> work"),
            ("show-notes-tags", "Show note tags", "show-notes-tags <note_id>"),
            ("search-notes-by-tag", "Find notes by tag", "search-notes-by-tag work"),
            ("sort-notes-by-tags", "Sort notes by tags", "sort-notes-by-tags"),
            ("all-notes-tags", "Show all tags", "all-notes-tags"),
        ],
    ),
]


def build_welcome_message() -> str:
    return (
        f"{APP_BANNER}\n"
        f"{APP_SUBTITLE}\n\n"
        f"{APP_HINT}\n"
        f"{HELP_GLOBAL_HINT}\n"
        f"{HELP_CONTACTS_HINT}\n"
        f"{HELP_NOTES_HINT}\n"
        f"{HELP_TAGS_HINT}"
    )


def build_help_message(section: str | None = None) -> str:
    normalized_section = section.lower() if section else None
    blocks = []
    section_hints = {
        "global": HELP_GLOBAL_HINT,
        "contacts": HELP_CONTACTS_HINT,
        "notes": HELP_NOTES_HINT,
        "tags": HELP_TAGS_HINT,
    }

    for section_name, rows in COMMAND_GROUPS:
        if normalized_section and section_name.lower() != normalized_section:
            continue
        colored_rows = []
        for command, description, example in rows:
            colored_rows.append(
                {
                    "Command": table_cell_colored_value(
                        command, HELP_TEXT_COLOR, HELP_BORDER_COLOR
                    ),
                    "Description": table_cell_colored_value(
                        description, HELP_TEXT_COLOR, HELP_BORDER_COLOR
                    ),
                    "Example": table_cell_colored_value(
                        example, HELP_TEXT_COLOR, HELP_BORDER_COLOR
                    ),
                }
            )
        table = AnsiColor.wrap(
            tabulate(colored_rows, headers="keys", tablefmt="fancy_grid"),
            HELP_BORDER_COLOR,
        )
        section_title = AnsiColor.wrap(section_name, HELP_TEXT_COLOR)
        blocks.append(f"{section_title}\n{table}")

    if normalized_section:
        hint = section_hints[normalized_section]
        return f"{hint}\n\n{''.join(blocks)}"

    return "\n\n".join(blocks)
