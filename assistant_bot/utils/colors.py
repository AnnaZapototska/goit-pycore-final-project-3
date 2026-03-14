from enum import Enum

class AnsiColor(str, Enum):
    """ANSI escape codes for terminal coloring (no external deps)."""

    RESET = "\x1b[0m"

    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"

    BRIGHT_BLACK = "\x1b[90m"
    BRIGHT_RED = "\x1b[91m"
    BRIGHT_GREEN = "\x1b[92m"
    BRIGHT_YELLOW = "\x1b[93m"
    BRIGHT_BLUE = "\x1b[94m"
    BRIGHT_MAGENTA = "\x1b[95m"
    BRIGHT_CYAN = "\x1b[96m"
    BRIGHT_WHITE = "\x1b[97m"

    # Optional styles
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    UNDERLINE = "\x1b[4m"

    @staticmethod
    def wrap(text: str, color: "AnsiColor") -> str:
        """Wrap text with one or more ANSI codes and reset at the end."""
        return AnsiColor.RESET + color + text + AnsiColor.RESET
    
def print_colored(text: str, color = AnsiColor.BRIGHT_CYAN):
    """Print text wrapped in the specified ANSI color."""
    print(AnsiColor.wrap(text, color))

def input_colored(prompt: str, color = AnsiColor.BRIGHT_CYAN) -> str:
    """Get user input with a colored prompt."""
    return input(AnsiColor.wrap(prompt, color) + AnsiColor.BRIGHT_BLUE)
