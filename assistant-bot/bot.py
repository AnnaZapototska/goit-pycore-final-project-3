from models.contacts import AddressBook, Record
from models.fields import Email, Phone, Address
from utils.decorators import input_error, require_args


@input_error
def hello_command(args, book: AddressBook):
    return "How can I help you?"


@input_error
@require_args(3, "add <name> <phone> <email>")
def add_contact(args, book: AddressBook):
    name, phone, email = args[:3]
    record = book.find(name)
    message = "Contact updated."

    validated_phone = Phone(phone) if phone else None
    validated_email = Email(email) if email else None

    if validated_email:
        book.ensure_email_unique(
            validated_email.value,
            owner_name=record.name.value if record else None
        )

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


@input_error
@require_args(2, "change <name> <phone>")
def change_command(args, book: AddressBook):
    name, phone = args
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    validated_phone = Phone(phone)

    if not record.phones:
        record.add_phone(validated_phone.value)
        return "Phone number added."

    old_phone = record.phones[0].value
    record.edit_phone(old_phone, validated_phone.value)
    return "Phone number updated."


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


@input_error
@require_args(1, "add-address <name>")
def add_address_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    full_address = build_address()
    record.add_address(full_address)
    return "Address added."


@input_error
@require_args(1, "edit-address <name>")
def edit_address_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    full_address = build_address()
    record.edit_address(full_address)
    return "Address updated."


@input_error
@require_args(1, "show-address <name>")
def show_address_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    address = record.get_address()
    if not address or address == "no address":
        return f"{name} has no address saved."

    return f"{name}'s address is {address}."


@input_error
@require_args(1, "remove-address <name>")
def remove_address_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    address = record.get_address()
    if not address or address == "no address":
        return "No address found."

    record.remove_address()
    return "Address removed."


@input_error
@require_args(1, "phone <name>")
def phone_command(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    if not record.phones:
        return "No phone numbers found."

    return f"{name}'s phone number is {record.phones[0].value}."

@input_error
def search_command(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Usage: search <query>")
    
    query = args[0]
    results = book.search(query)
    if not results:
        return "No contacts found."
    return "\n".join(str(record) for record in results)

@input_error
@require_args(2, "add-birthday <name> <birthday in DD.MM.YYYY>")
def add_birthday(args, book: AddressBook):
    name, birthdays = args
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    record.add_birthday(birthdays)
    return "Birthday added."


@input_error
@require_args(1, "show-birthday <name>")
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ValueError("Contact does not exist.")

    if not record.birthday:
        return "Birthday is not set for this contact."

    return f"{name}'s birthday is on {record.birthday.value}."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "Upcoming birthdays: " + ", ".join(upcoming)

def build_address():
    street = input("Enter street: ").strip()
    if not street:
        raise ValueError("Street cannot be empty.")

    city = input("Enter city: ").strip()
    if not city:
        raise ValueError("City cannot be empty.")

    country = input("Enter country: ").strip()
    if not country:
        raise ValueError("Country cannot be empty.")

    full_address = f"{street}, {city}, {country}"
    Address(full_address)  # validation
    return full_address


@input_error
def all_command(args, book: AddressBook):
    if not book:
        raise KeyError

    return "\n".join(str(record) for record in book.values())

# Exit the bot
@input_error
def close_command(args, book: AddressBook):
    return "Good bye!"


@input_error
def invalid_command(args, book: AddressBook):
    return "Invalid command."