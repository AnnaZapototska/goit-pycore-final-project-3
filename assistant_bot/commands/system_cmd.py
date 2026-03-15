from assistant_bot.utils.decorators import input_error, require_args
from assistant_bot.models.contacts import AddressBook       
from assistant_bot.utils.help_view import build_help_message


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

@input_error
@require_args(0, "help-global")
def help_global_command(args, book: AddressBook):
    return build_help_message("global")

@input_error
@require_args(0, "help-contacts")
def help_contacts_command(args, book: AddressBook):
    return build_help_message("contacts")


@input_error
@require_args(0, "help-notes")
def help_notes_command(args, book: AddressBook):
    return build_help_message("notes")


@input_error
@require_args(0, "help-tags")
def help_tags_command(args, book: AddressBook):
    return build_help_message("tags")

@input_error
@require_args(0, "help-groups")
def help_groups_command(args, book: AddressBook):
    return build_help_message("groups")