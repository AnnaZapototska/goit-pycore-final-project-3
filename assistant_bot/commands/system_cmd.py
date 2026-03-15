from utils.decorators import input_error, require_args
from models.contacts import AddressBook       
from utils.help_view import build_help_message


@input_error
@require_args(0, "hello")
def hello_command(args, book: AddressBook):
    """
    Simple greeting command.
    """
    return "How can I help you?"


@input_error
@require_args(0, "help")
def help_command(args, book: AddressBook):
    """
    Shows help message with available commands.
    """
    return build_help_message()


@input_error
@require_args(0, "close / exit")
def close_command(args, book):
    """
    Exits the bot.
    """
    return "Good bye!"


@input_error
def invalid_command(args, book):
    """
    Handles unknown commands.
    """
    return "Invalid command."

