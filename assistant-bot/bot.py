from models.contacts import AddressBook, Record
from models.fields import Email, Phone
from utils.decorators import input_error, require_args


# Greet the bot
@input_error
def hello_command(args, book: AddressBook):
    return "How can I help you?"

# Add a new contact with the given username, phone number, and email
@input_error
@require_args(3, "add <name> <phone> <email>")
def add_contact(args, book: AddressBook):
    name, phone, email = args[:3]
    record = book.find(name)
    message = "Contact updated."

    validated_phone = Phone(phone) if phone else None
    validated_email = Email(email) if email else None
    if validated_email:
        book.ensure_email_unique(validated_email.value, owner_name=record.name.value if record else None)

    if record is None:
        record = Record(name)
        message = "Contact added."

    if validated_phone:
        record.add_phone(validated_phone.value)

    if validated_email:
        if getattr(record, "email", None) is None:
            record.add_email(validated_email.value)
        else:
            record.edit_email(validated_email.value)

    if book.find(name) is None:
        book.add_record(record)

    return message


# Update the phone number of an existing contact
@input_error
@require_args(2, "change <name> <phone>")
def change_command(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")
    
    if not record.phones:
        return "No phone numbers found."
    return f"{name}'s phone number is {record.phones[0].value}."


@input_error
@require_args(2, "change-email <name> <new_email>")
def change_email_command(args, book: AddressBook):
    name, new_email = args[:2]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    validated_email = Email(new_email)
    book.ensure_email_unique(validated_email.value, owner_name=record.name.value)
    if getattr(record, "email", None) is None:
        record.add_email(validated_email.value)
    else:
        record.edit_email(validated_email.value)
    return "Email updated."


# Show the phone number for the specified contact
@input_error
@require_args(1, "phone <name>")
def phone_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError("Contact does not exist.")
    return f"{name}'s phone number is {record.phones[0].value}."


# add-birthday — add to contact DD.MM.YYYY
@input_error
@require_args(2, "add-birthday <name> <birthday in DD.MM.YYYY>")
def add_birthday(args, book: AddressBook):
    name, birthdays = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact does not exist.")     
    record.add_birthday(birthdays)
    return "Birthday added."
    
# show the date of birth
@input_error
@require_args(1, "show-birthday <name>")
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")
    return f"{name}'s birthday is on {record.birthday.value}."

# birthdays — return the list of the users with birthdays
@input_error
def birthdays(args, book: AddressBook):
    return "Upcoming birthdays: " + ", ".join(book.get_upcoming_birthdays())

# Display all saved contacts with phone numbers and email
@input_error
def all_command(args, book: AddressBook):
    if not book:
        raise KeyError

    return "\n".join(str(record) for record in book.values())

@input_error
def search_command(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Usage: search <query>")
    
    query = args[0]
    results = book.search(query)
    if not results:
        return "No contacts found."
    return "\n".join(str(record) for record in results)

# Exit the bot
@input_error
def close_command(args, book: AddressBook):
    return "Good bye!"

# For invalid commands
@input_error
def invalid_command(args, book: AddressBook):
    return "Invalid command."
