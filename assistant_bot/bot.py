from models.contacts import AddressBook, Record
from models.notes import NotesBook, Note
from models.fields import Email, Phone, Address
from utils.decorators import input_error, require_args


@input_error
@require_args(0, "hello")
def hello_command(args, book: AddressBook):
    return "How can I help you?"


def resolve_record(selector, book: AddressBook):
    # Resolve a contact using either phone or email.
    record = book.find_by_selector(selector)
    if record is None:
        raise ValueError("Contact not found")
    return record


def apply_contact_edit(record, field, new_value, book: AddressBook):
    # Normalize the requested field name so command input is case-insensitive.
    normalized_field = field.strip().lower()

    if normalized_field == "name":
        # Update only the contact name.
        record.set_name(new_value)
        return "Name updated."

    if normalized_field == "add-phone":
        # Validate and add a new non-primary phone to the existing contact.
        validated_phone = Phone(new_value)
        book.ensure_phone_unique(validated_phone.value)
        record.add_phone(validated_phone.value)
        return "Phone added."

    if normalized_field == "email":
        # Validate email and keep it globally unique across contacts.
        validated_email = Email(new_value)
        book.ensure_email_unique(
            validated_email.value,
            owner_phone=record.primary_phone.value
        )

        if getattr(record, "email", None) is None:
            record.add_email(validated_email.value)
        else:
            record.edit_email(validated_email.value)

        return "Email updated."

    if normalized_field == "address":
        # Validate and update the contact address.
        validated_address = Address(new_value)

        if getattr(record, "address", None) is None:
            record.add_address(validated_address.value)
        else:
            record.edit_address(validated_address.value)

        return "Address updated."

    if normalized_field == "birthday":
        # Reuse the existing birthday validator from the Birthday field.
        record.add_birthday(new_value)
        return "Birthday updated."

    raise ValueError(
        "Unsupported field. Use name, add-phone, email, address, or birthday."
    )


# ADD CONTACT
@input_error
def add_contact(args, book: AddressBook):
    if len(args) not in (2, 3):
        return "Usage: add <name> <phone> [email]"

    name, phone = args[:2]
    email = args[2] if len(args) == 3 else None

    validated_phone = Phone(phone)
    validated_email = Email(email) if email else None
    existing_record = book.find(validated_phone.value)
    if existing_record is not None:
        raise ValueError("A contact with this phone number already exists")

    if validated_email:
        book.ensure_email_unique(validated_email.value)

    record = Record(name, validated_phone.value)

    if validated_email:
        record.add_email(validated_email.value)

    book.add_record(record)
    return "Contact added."


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


@input_error
def edit_command(args, book: AddressBook):
    # Support values with spaces, for example full names or addresses.
    if len(args) < 3:
        return "Usage: edit <phone_or_email> <field> <new_value>"

    selector = args[0]
    field = args[1]
    new_value = " ".join(args[2:]).strip()

    if not new_value:
        raise ValueError("New value cannot be empty.")

    record = resolve_record(selector, book)
    return apply_contact_edit(record, field, new_value, book)


# PHONE
@input_error
@require_args(1, "phone <phone_or_email>")
def phone_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book)
    return f"{record.name.value}'s primary " + \
        f"phone number is {record.primary_phone.value}."

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

# --- notes commands ---

@input_error
@require_args(1, "add_note <title> <text>")
def add_note_command(args, notes_book: NotesBook):
    """
    Adds a note to NotesBook.
    """
    if len(args) == 1:
        # Only text provided, use default title
        title = None
        text = args[0]
    else:
        title = args[0]
        text = " ".join(args[1:])

    notes_book.add_note(title, text)
    return f"Note '{title or 'Untitled'}' added successfully."

@input_error
@require_args(0, "show_notes")
def show_notes_command(args, notes_book: NotesBook):
    """
    Shows all notes.
    """
    if not notes_book:
        return "No notes found."
    return str(notes_book)


@input_error
@require_args(2, "edit_note <title> <new_text>")
def edit_note_command(args, notes_book: NotesBook):
    """
    Edits the text of a note.
    """
    title = args[0]
    new_text = " ".join(args[1:])

    notes_book.edit_note(title, new_text)
    return f"Note '{title}' updated successfully."

@input_error
@require_args(1, "delete_note <title>")
def delete_note_command(args, notes_book: NotesBook):
    """
    Deletes a note by title.
    Usage: delete_note <title>
    """
    title = args[0]
    notes_book.delete_note(title)
    return f"Note '{title}' deleted successfully."


@input_error
@require_args(1, "search_notes <keyword>")
def search_notes_command(args, notes_book: NotesBook):
    """
    Searches notes by keyword in title or text.
    Usage: search_notes <keyword>
    """
    keyword = args[0]
    results = notes_book.search_notes(keyword)
    if not results:
        return f"No notes found matching '{keyword}'."
    return "\n".join(str(note) for note in results)

