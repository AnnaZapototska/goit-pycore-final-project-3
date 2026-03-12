from models.contacts import AddressBook, Record
from models.fields import Email, Phone, Address
from utils.decorators import input_error, require_args


@input_error
@require_args(0, "hello")
def hello_command(args, book: AddressBook):
    return "How can I help you?"


def resolve_record(selector, book: AddressBook):
    record = book.find_by_selector(selector)
    if record is None:
        raise ValueError("Contact does not exist.")
    return record


# ADD CONTACT
@input_error
def add_contact(args, book: AddressBook):
    if len(args) not in (2, 3):
        return "Usage: add <name> <phone> [email]"

    name, phone = args[:2]
    email = args[2] if len(args) == 3 else None

    validated_phone = Phone(phone)
    validated_email = Email(email) if email else None

    record = book.find(validated_phone.value)
    message = "Contact updated."

    if validated_email:
        book.ensure_email_unique(
            validated_email.value,
            owner_phone=record.primary_phone.value if record else None
        )

    if validated_phone:
        book.ensure_phone_unique(
            validated_phone.value,
            owner_name=record.name.value if record else None
        )

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


# CHANGE PHONE
@input_error
@require_args(2, "change <phone_or_email> <new_phone>")
def change_command(args, book: AddressBook):
    selector, new_phone = args
    record = resolve_record(selector, book)
    book.replace_primary_phone(record.primary_phone.value, new_phone)
    return "Primary phone updated."


# CHANGE EMAIL
@input_error
@require_args(2, "change-email <phone_or_email> <new_email>")
def change_email_command(args, book: AddressBook):
    selector, new_email = args

    record = resolve_record(selector, book)
    validated_email = Email(new_email)

    book.ensure_email_unique(
        validated_email.value,
        owner_phone=record.primary_phone.value
    )

    if getattr(record, "email", None) is None:
        record.add_email(validated_email.value)
    else:
        record.edit_email(validated_email.value)

    return "Email updated."


# PHONE
@input_error
@require_args(1, "phone <phone_or_email>")
def phone_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)
    return f"{record.name.value}'s primary phone number is {record.primary_phone.value}."


# SEARCH
@input_error
def search_command(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("Usage: search <query>")

    query = args[0]
    results = book.search(query)

    if not results:
        return "No contacts found."

    return "\n".join(str(record) for record in results)


# ADDRESS HELPERS
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
    Address(full_address)
    return full_address


# ADD ADDRESS
@input_error
@require_args(1, "add-address <phone_or_email>")
def add_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)

    full_address = build_address()
    record.add_address(full_address)

    return "Address added."


# EDIT ADDRESS
@input_error
@require_args(1, "edit-address <phone_or_email>")
def edit_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)

    full_address = build_address()
    record.edit_address(full_address)

    return "Address updated."


# SHOW ADDRESS
@input_error
@require_args(1, "show-address <phone_or_email>")
def show_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)

    address = record.get_address()

    if not address or address == "no address":
        return f"{record.name.value} has no address saved."

    return f"{record.name.value}'s address is {address}."


# REMOVE ADDRESS
@input_error
@require_args(1, "remove-address <phone_or_email>")
def remove_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)

    address = record.get_address()

    if not address or address == "no address":
        return "No address found."

    record.remove_address()

    return "Address removed."

@input_error
@require_args(1, "search <query>")
def search_command(args, book: AddressBook):
    query = args[0]
    results = book.search(query)
    if not results:
        return "No contacts found."
    return "\n".join(str(record) for record in results)

# BIRTHDAY
@input_error
@require_args(2, "add-birthday <phone_or_email> <DD.MM.YYYY>")
def add_birthday(args, book: AddressBook):
    selector, birthday = args

    record = resolve_record(selector, book)
    record.add_birthday(birthday)

    return "Birthday added."


@input_error
@require_args(1, "show-birthday <phone_or_email>")
def show_birthday(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)

    if not record.birthday:
        return "Birthday is not set for this contact."

    # Format date object to DD.MM.YYYY
    birthday_str = record.birthday.value.strftime("%d.%m.%Y")
    return f"{record.name.value}'s birthday is on {birthday_str}."


@input_error
@require_args(0, "birthdays")
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    return "Upcoming birthdays: " + ", ".join(upcoming)


# SHOW ALL
@input_error
@require_args(0, "all")
def all_command(args, book: AddressBook):
    if not book:
        raise KeyError

    return "\n".join(str(record) for record in book.iter_records())


# EXIT
@input_error
@require_args(0, "close / exit")
def close_command(args, book: AddressBook):
    return "Good bye!"


# INVALID
@input_error
def invalid_command(args, book: AddressBook):
    return "Invalid command."