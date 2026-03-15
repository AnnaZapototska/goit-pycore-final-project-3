from assistant_bot.models.contacts import AddressBook
from assistant_bot.models.fields import Address
from assistant_bot.utils.decorators import input_error, require_args
from assistant_bot.utils.colors import AnsiColor
from assistant_bot.bot import resolve_record, apply_contact_edit
from assistant_bot.services.contacts_service import ContactService


# SHOW ALL
@input_error
@require_args(0, "all")
def all_command(args, book: AddressBook):
    """Displays all contacts in a formatted table."""

    if not book or not book.data:
        return "No contacts found."

    return book.to_table(
        text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    )


# --- SEARCH CONTACT ---
@input_error
@require_args(1, "search <query>")
def search_command(args, book: AddressBook):
    """Searches for contacts matching the query in name, phone, or email."""
    query = args[0]
    
    service = ContactService(book)
    results = service.search(query)

    if not results:
        return "No contacts found."

    return results.to_table()

# --- ADD CONTACT ---
@input_error
def add_contact_command(args, book: AddressBook):
    """Adds a new contact with the provided name, phone, and optional email."""

    if len(args) not in (2, 3):
        return "Usage: add <name> <phone> [email]"

    name, phone = args[:2]
    email = args[2] if len(args) == 3 else None

    service = ContactService(book)
    record = service.add_contact(name, phone, email)

    return f"Contact added: ID [{record.id}], Name {record.name.value}"


# --- CHANGE PRIMARY PHONE ---
@input_error
@require_args(2, "edit <id> <new_phone>")
def change_command(args, book: AddressBook):
    """Changes the primary phone number for a contact."""

    record_id, new_phone = args

    service = ContactService(book)
    service.change_primary_phone(record_id, new_phone)
    return "Primary phone updated."


# --- CHANGE EMAIL ---
@input_error
@require_args(2, "edit-email <id> <new_email>")
def change_email_command(args, book: AddressBook):
    """Edits the contact's email."""

    record_id, new_email = args
    record = resolve_record(record_id, book, require_id_only=True)

    service = ContactService(book)
    service.change_email(record, new_email)

    return "Email updated."


# --- EDIT PHONE ---
@input_error
@require_args(3, "edit-phone <id> <old_phone> <new_phone>")
def edit_phone_command(args, book: AddressBook):
    """Edits a specific phone number for a contact."""

    record_id, old_phone, new_phone = args
    record = resolve_record(record_id, book, require_id_only=True)

    service = ContactService(book)
    service.edit_phone(record, old_phone, new_phone)

    return "Phone updated."


# --- EDIT GENERIC ---
@input_error
def edit_command(args, book: AddressBook):
    """Edit contact."""

    if len(args) < 3:
        return "Usage: edit <id_or_phone_or_email> <field> <new_value>"

    selector = args[0]
    field = args[1]
    new_value = " ".join(args[2:]).strip()

    if not new_value:
        raise ValueError("New value cannot be empty.")

    record = resolve_record(selector, book)
    return apply_contact_edit(record, field, new_value, book)


# --- SHOW PRIMARY PHONE ---
@input_error
@require_args(1, "show-primary-phone <id_or_phone_or_email>")
def phone_command(args, book: AddressBook):
    """Shows the primary phone number for a contact."""

    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    return f"{record.name.value}'s primary phone number is {record.primary_phone.value}"


# --- SHOW ALL PHONES ---
@input_error
@require_args(1, "show-phone <id_or_phone_or_email>")
def show_phone_command(args, book: AddressBook):
    """Shows all phone numbers for a contact."""
    
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    return f"{record.name.value}'s phone numbers: {record.get_phones_display()}"


# --- DELETE CONTACT ---
@input_error
@require_args(1, "delete <id>")
def delete_contact_command(args, book: AddressBook):
    """Deletes a contact by its ID after confirmation."""

    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    service = ContactService(book)

    while True:
        confirm = input(
            f"Are you sure you want to delete contact '{record.name.value}' [ID: {record.id}]? (Y/N): "
        ).strip().lower()

        if confirm in ("y", "yes"):
            service.delete_contact(record_id)
            return "Contact deleted."

        if confirm in ("n", "no"):
            return "Delete canceled."

        print("Please enter Y or N.")


# --- ADDRESS HELPERS ---
def build_address():
    """Prompts the user to enter address details and constructs a full address string."""

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


# --- ADD ADDRESS ---
@input_error
@require_args(1, "add-address <id>")
def add_address_command(args, book: AddressBook):
    """Adds an address to the contact."""

    selector = args[0]
    service = ContactService(book)
    record = resolve_record(selector, book, require_id_only=False)
    full_address = build_address()
    service.add_address(record, full_address)
    return "Address added."


# --- EDIT ADDRESS ---
@input_error
@require_args(1, "edit-address <id>")
def edit_address_command(args, book: AddressBook):
    """Edits the contact's address."""

    selector = args[0]
    service = ContactService(book)
    record = resolve_record(selector, book, require_id_only=False)
    full_address = build_address()
    service.edit_address(record, full_address)
    return "Address updated."


# --- SHOW ADDRESS ---
@input_error
@require_args(1, "show-address <id>")
def show_address_command(args, book: AddressBook):
    """Shows the contact's address."""
    selector = args[0]
    service = ContactService(book)
    record = resolve_record(selector, book, require_id_only=False)
    address = service.get_address(record)

    if not address or address == "no address":
        return f"{record.name.value} has no address saved."

    return f"{record.name.value}'s address is {address}"


# --- REMOVE ADDRESS ---
@input_error
@require_args(1, "remove-address <id>")
def remove_address_command(args, book: AddressBook):
    """Removes the contact's address."""
    selector = args[0]
    service = ContactService(book)
    record = resolve_record(selector, book, require_id_only=False)
    address = service.get_address(record)

    if not address or address == "no address":
        return "No address found."

    service.remove_address(record)
    return "Address removed."


# --- BIRTHDAY ---
@input_error
@require_args(2, "add-birthday <id> <DD.MM.YYYY>")
def add_birthday_command(args, book: AddressBook):
    """Adds a birthday to the contact."""
    selector, birthday = args
    record = resolve_record(selector, book, require_id_only=False)
    service = ContactService(book)
    service.add_birthday(record, birthday)
    return "Birthday added."


@input_error
@require_args(1, "show-birthday <id>")
def show_birthday_command(args, book: AddressBook):
    """Shows the contact's birthday."""
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    service = ContactService(book)

    if not record.birthday:
        return "Birthday is not set for this contact."

    birthday_str = record.birthday.value.strftime("%d.%m.%Y")
    return f"{record.name.value}'s birthday is on {birthday_str}"


@input_error
def birthdays_command(args, book: AddressBook):
    """Show upcoming birthdays within a specified number of days, sorted by date."""
    days_ahead = 7

    if args:
        try:
            days_ahead = int(args[0])
        except ValueError:
            raise ValueError("Please provide a valid number of days.")

    upcoming_list = book.get_upcoming_birthdays(days_ahead=days_ahead)

    if not upcoming_list:
        return f"No upcoming birthdays within the next {days_ahead} days."

    temp_book = AddressBook()
    for record, _ in upcoming_list:
        temp_book.data[record.id] = record

    return temp_book.to_table(
        text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    )

# --- GROUPS ---
@input_error
@require_args(1, "add-group <group>")
def add_group_command(args, book: AddressBook):
    """Adds a new group to the system."""
    group = args[0]

    service = ContactService(book)
    normalized_group = service.add_group(group)

    return f"Group '{normalized_group}' added."


@input_error
@require_args(0, "all-groups")
def all_groups_command(args, book: AddressBook):
    """Shows all groups in the system."""
    groups = book.get_all_groups()

    if not groups:
        return "No groups found."

    return "Available groups: " + ", ".join(groups)


@input_error
@require_args(1, "delete-group <group>")
def delete_group_command(args, book: AddressBook):
    """Deletes a group and removes it from all contacts."""
    group = args[0]
    normalized_group = book.normalize_group_name(group)
    service = ContactService(book)

    while True:
        confirm = input(
            f"Are you sure you want to delete group '{normalized_group}' from the system and all contacts? (Y/N): "
        ).strip().lower()

        if confirm in ("y", "yes"):
            normalized_group = service.delete_group(group)
            return f"Group '{normalized_group}' deleted."

        if confirm in ("n", "no"):
            return "Delete canceled."

        print("Please enter Y or N.")


@input_error
@require_args(2, "add-contact-group <contact_id> <group>")
def add_contact_group_command(args, book: AddressBook):
    """Add group to a contact."""
    record_id, group = args
    service = ContactService(book)
    normalized_group = service.add_contact_to_group(record_id, group)
    return f"Contact ID [{record_id}] added to group '{normalized_group}'."


@input_error
@require_args(1, "add-contacts-to-group <group> <contact_id_1> <contact_id_2> ...")
def add_contacts_to_group_command(args, book: AddressBook):
    """Adds multiple contacts to a group."""

    if not args:
        return "Usage: add-contacts-to-group <group> <contact_id_1> <contact_id_2> ..."

    group = args[0]
    record_ids = args[1:]

    if not record_ids:
        return "Usage: add-contacts-to-group <group> <contact_id_1> <contact_id_2> ..."

    result = book.add_contacts_to_group(group, record_ids)

    lines = [f"Group: {result['group']}"]

    if result["added"]:
        lines.append("Added: " + ", ".join(result["added"]))

    if result["skipped"]:
        lines.append("Skipped: " + ", ".join(result["skipped"]))

    return "\n".join(lines)


@input_error
@require_args(2, "delete-contact-group <contact_id> <group>")
def delete_contact_group_command(args, book: AddressBook):
    """Removes a contact from a specific group."""

    record_id, group = args
    service = ContactService(book)
    normalized_group = service.remove_contact_from_group(record_id, group)
    return f"Contact ID [{record_id}] removed from group '{normalized_group}'."


@input_error
@require_args(1, "delete-contact-groups <contact_id>")
def delete_contact_groups_command(args, book: AddressBook):
    """Removes all groups from a contact."""

    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return "Contact has no groups."

    record.clear_groups()
    return f"All groups removed from contact ID [{record_id}]."


@input_error
@require_args(1, "show-contact-groups <contact_id>")
def show_contact_groups_command(args, book: AddressBook):
    """Shows all groups that a contact belongs to."""

    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return f"{record.name.value} has no groups."

    return f"{record.name.value}'s groups: {record.get_groups_display()}"


@input_error
@require_args(1, "search-contacts-by-group <group>")
def search_contacts_by_group_command(args, book: AddressBook):
    """Searches for contacts that belong to a specific group."""

    group = args[0]
    normalized_group = book.normalize_group_name(group)
    results = book.find_contacts_by_group(normalized_group)

    if not results:
        return f"No contacts found in group '{normalized_group}'."

    return results.to_table()