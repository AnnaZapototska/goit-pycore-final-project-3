from tabulate import tabulate
from utils.colors import AnsiColor

GREEN_FILL = AnsiColor.GREEN.value
GREEN_SHADOW = AnsiColor.BRIGHT_BLACK.value
RESET = AnsiColor.RESET.value

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
APP_HINT = 'Type "help" to see commands'

COMMAND_GROUPS = [
    (
        "Global",
        [
            ("hello", "Show a short greeting", "hello"),
            ("help", "Show all available commands", "help"),
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
            ("edit-contact", "Edit a contact field", "edit-contact 1234567890 email new@mail.com"),
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
    return f"{APP_BANNER}\n{APP_SUBTITLE}\n\n{APP_HINT}"


def build_help_message() -> str:
    blocks = []

    for section_name, rows in COMMAND_GROUPS:
        headers = ["Command", "Description", "Example"]
        table = tabulate(rows, headers=headers, tablefmt="fancy_grid")
        blocks.append(f"{section_name}\n{table}")

    return "\n\n".join(blocks)
