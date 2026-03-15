from difflib import get_close_matches
from typing import Iterable, List, Tuple


def parse_input(user_input: str) -> Tuple[str, List[str]]:
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


def get_command_suggestions(
    command: str, available_commands: Iterable[str], limit: int = 3
) -> List[str]:
    """
    Return a list of the closest valid commands for mistyped user input.
    First try prefix matching, then fuzzy matching.
    """
    if not command or len(command.strip()) < 2:
        return []

    # Prefix matching for short forms like "sho" -> "show-address"
    commands_list = list(available_commands)
    prefix_matches = [cmd for cmd in commands_list if cmd.startswith(command)]

    # Fuzzy matching for typos like "sho-address" -> "show-address"
    fuzzy_matches = get_close_matches(command, commands_list, n=limit, cutoff=0.6)

    # Merge results without duplicates while preserving order
    suggestions = []
    for cmd in prefix_matches + fuzzy_matches:
        if cmd not in suggestions:
            suggestions.append(cmd)

    return suggestions[:limit]


def ask_confirmation() -> bool:
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
