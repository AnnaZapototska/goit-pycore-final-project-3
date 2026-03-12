from models.contacts import AddressBook, Record
from models.fields import Email, Phone
from utils.decorators import input_error, require_args


# Greet the bot
@input_error
def hello_command(args, book: AddressBook):
    return "How can I help you?"


def resolve_record(selector, book: AddressBook):
    record = book.find_by_selector(selector)
    if record is None:
        raise ValueError("Contact does not exist.")
    return record


# Add a new contact with the given username, phone number, and optional email
@input_error
def add_contact(args, book: AddressBook):
    if len(args) not in (2, 3):
        return "Usage: add <name> <phone> [email]"

    name, phone = args[:2]
    email = args[2] if len(args) == 3 else None
    validated_phone = Phone(phone)
    record = book.find(validated_phone.value)
    message = "Contact updated."

    validated_email = Email(email) if email else None
    if validated_email:
        book.ensure_email_unique(validated_email.value, owner_phone=record.primary_phone.value if record else None)

    if record is None:
        record = Record(name, validated_phone.value)
        message = "Contact added."
        if validated_email:
            record.add_email(validated_email.value)
        book.add_record(record)
        return message

    record.set_name(name)

    if validated_email:
        if getattr(record, "email", None) is None:
            record.add_email(validated_email.value)
        else:
            record.edit_email(validated_email.value)

    return message


# Update the phone number of an existing contact
@input_error
@require_args(2, "change <phone_or_email> <new_phone>")
def change_command(args, book: AddressBook):
    selector, new_phone = args
    record = resolve_record(selector, book)
    book.replace_primary_phone(record.primary_phone.value, new_phone)
    return "Primary phone updated."


@input_error
@require_args(2, "change-email <phone_or_email> <new_email>")
def change_email_command(args, book: AddressBook):
    selector, new_email = args[:2]
    record = resolve_record(selector, book)
    validated_email = Email(new_email)
    book.ensure_email_unique(validated_email.value, owner_phone=record.primary_phone.value)
    if getattr(record, "email", None) is None:
        record.add_email(validated_email.value)
    else:
        record.edit_email(validated_email.value)
    return "Email updated."


# Show the phone number for the specified contact
@input_error
@require_args(1, "phone <phone_or_email>")
def phone_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)
    return f"{record.name.value}'s primary phone number is {record.primary_phone.value}."


# add-birthday — add to contact DD.MM.YYYY
@input_error
@require_args(2, "add-birthday <phone_or_email> <birthday in DD.MM.YYYY>")
def add_birthday(args, book: AddressBook):
    selector, birthdays = args
    record = resolve_record(selector, book)
    record.add_birthday(birthdays)
    return "Birthday added."
    
# show the date of birth
@input_error
@require_args(1, "show-birthday <phone_or_email>")
def show_birthday(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)
    return f"{record.name.value}'s birthday is on {record.birthday.value}."

# birthdays — return the list of the users with birthdays
@input_error
def birthdays(args, book: AddressBook):
    return "Upcoming birthdays: " + ", ".join(book.get_upcoming_birthdays())

# Display all saved contacts with phone numbers and email
@input_error
def all_command(args, book: AddressBook):
    if not book:
        raise KeyError

    return "\n".join(str(record) for record in book.iter_records())

# Exit the bot
@input_error
def close_command(args, book: AddressBook):
    return "Good bye!"

# For invalid commands
@input_error
def invalid_command(args, book: AddressBook):
    return "Invalid command."
