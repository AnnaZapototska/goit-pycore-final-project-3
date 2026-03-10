from models.contacts import AddressBook, Record
from utils.decorators import input_error, require_args

# Greet the bot
@input_error
def hello_command(args, book: AddressBook):
    return "How can I help you?"

# Add a new contact with the given username and phone number
@input_error
@require_args(2, "add <name> <phone>")
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)  
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)
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

# Display all saved contacts with phone numbers
@input_error
def all_command(args, book: AddressBook):
    if not book:
        raise KeyError

    result = ""
    for name, record in book.items():
        phones = "; ".join(p.value for p in record.phones)
        result += f"{name}: {phones}\n"
    return result.strip()

# Exit the bot
@input_error
def close_command(args, book: AddressBook):
    return "Good bye!"

# For invalid commands
@input_error
def invalid_command(args, book: AddressBook):
    return "Invalid command."