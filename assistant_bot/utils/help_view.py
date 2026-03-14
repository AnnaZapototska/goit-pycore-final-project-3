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
            ("all", "Show all contacts", "all"),
            ("search", "Search contacts by query", "search John"),
            ("close", "Close the bot", "close"),
            ("exit", "Exit the bot", "exit"),
        ],
    ),
    (
        "Contacts",
        [
            ("add", "Add a new contact", "add John 1234567890 john@mail.com"),
            ("edit", "Edit a contact field", "edit 1234567890 email new@mail.com"),
            ("change", "Change the primary phone", "change <id> 0991234567"),
            ("change-email", "Change the contact email", "change-email <id> new@mail.com"),
            ("delete", "Delete a contact", "delete <id>"),
            ("phone", "Show the primary phone", "phone <id>"),
            ("add-address", "Add an address", "add-address <id>"),
            ("edit-address", "Update the address", "edit-address <id>"),
            ("show-address", "Show the address", "show-address <id>"),
            ("remove-address", "Remove the address", "remove-address <id>"),
            ("add-birthday", "Add a birthday", "add-birthday <id> 01.01.2000"),
            ("show-birthday", "Show the birthday", "show-birthday <id>"),
            ("birthdays", "Show upcoming birthdays", "birthdays"),
        ],
    ),
    (
        "Notes",
        [
            ("add_note", "Create a new note", "add_note"),
            ("show_notes", "Show all notes", "show_notes"),
            ("edit_note", "Edit a note", "edit_note <id>"),
            ("delete_note", "Delete a note", "delete_note <id>"),
            ("search_notes", "Search notes", "search_notes report"),
        ],
    ),
    (
        "Tags",
        [
            ("add-tag", "Add a tag to a note", "add-tag <note_id> work"),
            ("remove-tag", "Remove a tag from a note", "remove-tag <note_id> work"),
            ("show-tags", "Show note tags", "show-tags <note_id>"),
            ("search-tag", "Find notes by tag", "search-tag work"),
            ("sort-notes-by-tags", "Sort notes by tags", "sort-notes-by-tags"),
            ("all-tags", "Show all tags", "all-tags"),
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
