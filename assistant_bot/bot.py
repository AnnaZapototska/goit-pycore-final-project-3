from models.contacts import AddressBook, Record
from models.notes import NotesBook, NotesList
from models.fields import Email, Phone, Address
from utils.decorators import input_error, require_args
from utils.colors import AnsiColor
from utils.help_view import build_help_message

@input_error
@require_args(0, "hello")
def hello_command(args, book: AddressBook):
    return "How can I help you?"


@input_error
@require_args(0, "help")
def help_command(args, book: AddressBook):
    return build_help_message()


def resolve_record(selector, book: AddressBook, require_id_only=False):
    """Resolve contact by ID only or by selector (ID | phone | email)."""
    selector = str(selector).strip()

    if require_id_only:
        record = book.find_by_id(selector)
        if not record:
            raise ValueError(f"Contact ID {selector} not found")
    else:
        record = book.find_by_selector(selector)
        if not record:
            raise ValueError("Contact not found")
    return record


def apply_contact_edit(record, field, new_value, book: AddressBook):
    normalized_field = field.strip().lower()

    if normalized_field == "name":
        record.set_name(new_value)
        return "Name updated."

    if normalized_field == "add-phone":
        validated_phone = Phone(new_value)
        book.ensure_phone_unique(validated_phone.value, owner_record_id=record.id)
        record.add_phone(validated_phone.value)
        return "Phone added."

    if normalized_field == "email":
        validated_email = Email(new_value)
        book.ensure_email_unique(
            validated_email.value, owner_phone=record.primary_phone.value
        )

        if record.email is None:
            record.add_email(validated_email.value)
        else:
            record.edit_email(validated_email.value)

        return "Email updated."

    if normalized_field == "address":
        validated_address = Address(new_value)
        if record.address is None:
            record.add_address(validated_address.value)
        else:
            record.edit_address(validated_address.value)
        return "Address updated."

    if normalized_field == "birthday":
        record.add_birthday(new_value)
        return "Birthday updated."

    raise ValueError(
        "Unsupported field. Use name, add-phone, email, address, or birthday."
    )


# ADD CONTACT
@input_error
def add_contact_command(args, book: AddressBook):
    if len(args) not in (2, 3):
        return "Usage: add <name> <phone> [email]"

    name, phone = args[:2]
    email = args[2] if len(args) == 3 else None

    validated_phone = Phone(phone)
    validated_email = Email(email) if email else None

    book.ensure_phone_unique(validated_phone.value)

    if validated_email:
        book.ensure_email_unique(validated_email.value)

    record = Record(name, validated_phone.value)
    if validated_email:
        record.add_email(validated_email.value)

    book.add_record(record)
    return f"Contact added: ID [{record.id}], Name {record.name.value}"


# CHANGE PRIMARY PHONE
@input_error
@require_args(2, "change <id> <new_phone>")
def change_command(args, book: AddressBook):
    record_id, new_phone = args
    record = resolve_record(record_id, book, require_id_only=True)
    book.replace_primary_phone(record.id, new_phone)
    return "Primary phone updated."


# CHANGE EMAIL
@input_error
@require_args(2, "change-email <id> <new_email>")
def change_email_command(args, book: AddressBook):
    record_id, new_email = args
    record = resolve_record(record_id, book, require_id_only=True)

    validated_email = Email(new_email)
    book.ensure_email_unique(validated_email.value, record_id)

    if record.email is None:
        record.add_email(validated_email.value)
    else:
        record.edit_email(validated_email.value)

    return "Email updated."


# EDIT PHONE
@input_error
@require_args(3, "edit-phone <id> <old_phone> <new_phone>")
def edit_phone_command(args, book: AddressBook):
    record_id, old_phone, new_phone = args
    record = resolve_record(record_id, book, require_id_only=True)

    validated_new_phone = Phone(new_phone)
    book.ensure_phone_unique(validated_new_phone.value, owner_record_id=record.id)
    record.edit_phone(old_phone, validated_new_phone.value)

    return "Phone updated."


@input_error
def edit_command(args, book: AddressBook):
    if len(args) < 3:
        return "Usage: edit <id_or_phone_or_email> <field> <new_value>"

    selector = args[0]
    field = args[1]
    new_value = " ".join(args[2:]).strip()

    if not new_value:
        raise ValueError("New value cannot be empty.")

    record = resolve_record(selector, book)
    return apply_contact_edit(record, field, new_value, book)


# SHOW PRIMARY PHONE
@input_error
@require_args(1, "show-primary-phone <id_or_phone_or_email>")
def phone_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    return f"{record.name.value}'s primary phone number is {record.primary_phone.value}"

# SHOW ALL PHONES
@input_error
@require_args(1, "show-phone <id_or_phone_or_email>")
def show_phone_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    return f"{record.name.value}'s phone numbers: {record.get_phones_display()}"

# DELETE CONTACT
@input_error
@require_args(1, "delete <id>")
def delete_contact_command(args, book: AddressBook):
    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    while True:
        confirm = (
            input(
                f"Are you sure you want to delete contact '{record.name.value}' [ID: {record.id}]? (Y/N): "
            )
            .strip()
            .lower()
        )
        if confirm in ("y", "yes"):
            book.delete(record.id)
            return "Contact deleted."

        if confirm in ("n", "no"):
            return "Delete canceled."

        print("Please enter Y or N.")


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
@require_args(1, "add-address <id>")
def add_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)

    full_address = build_address()
    record.add_address(full_address)

    return "Address added."


# EDIT ADDRESS
@input_error
@require_args(1, "edit-address <id>")
def edit_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    full_address = build_address()
    record.edit_address(full_address)
    return "Address updated."


# SHOW ADDRESS
@input_error
@require_args(1, "show-address <id>")
def show_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
    address = record.get_address()

    if not address or address == "no address":
        return f"{record.name.value} has no address saved."

    return f"{record.name.value}'s address is {address}"


# REMOVE ADDRESS
@input_error
@require_args(1, "remove-address <id>")
def remove_address_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)
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

    return results.to_table()


# BIRTHDAY
@input_error
@require_args(2, "add-birthday <id> <DD.MM.YYYY>")
def add_birthday_command(args, book: AddressBook):
    selector, birthday = args
    record = resolve_record(selector, book, require_id_only=False)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
@require_args(1, "show-birthday <id>")
def show_birthday_command(args, book: AddressBook):
    selector = args[0]
    record = resolve_record(selector, book, require_id_only=False)

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


# GROUPS

@input_error
@require_args(1, "add-group <group>")
def add_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)
    book.add_group(normalized_group)
    return f"Group '{normalized_group}' added."


@input_error
@require_args(0, "all-groups")
def all_groups_command(args, book: AddressBook):
    groups = book.get_all_groups()

    if not groups:
        return "No groups found."

    return "Available groups: " + ", ".join(groups)


@input_error
@require_args(1, "delete-group <group>")
def delete_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)

    while True:
        confirm = input(
            f"Are you sure you want to delete group '{normalized_group}' from the system and all contacts? (Y/N): "
        ).strip().lower()

        if confirm in ("y", "yes"):
            book.delete_group(normalized_group)
            return f"Group '{normalized_group}' deleted."

        if confirm in ("n", "no"):
            return "Delete canceled."

        print("Please enter Y or N.")


@input_error
@require_args(2, "add-contact-group <contact_id> <group>")
def add_contact_group_command(args, book: AddressBook):
    record_id, group = args
    normalized_group = book.normalize_group_name(group)
    book.add_contact_to_group(record_id, normalized_group)
    return f"Contact ID [{record_id}] added to group '{normalized_group}'."


@input_error
@require_args(1, "add-contacts-to-group <group> <contact_id_1> <contact_id_2> ...")
def add_contacts_to_group_command(args, book: AddressBook):
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
    record_id, group = args
    normalized_group = book.normalize_group_name(group)
    book.delete_contact_group(record_id, normalized_group)
    return f"Contact ID [{record_id}] removed from group '{normalized_group}'."


@input_error
@require_args(1, "delete-contact-groups <contact_id>")
def delete_contact_groups_command(args, book: AddressBook):
    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return "Contact has no groups."

    record.clear_groups()
    return f"All groups removed from contact ID [{record_id}]."


@input_error
@require_args(1, "show-contact-groups <contact_id>")
def show_contact_groups_command(args, book: AddressBook):
    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return f"{record.name.value} has no groups."

    return f"{record.name.value}'s groups: {record.get_groups_display()}"


@input_error
@require_args(1, "search-contacts-by-group <group>")
def search_contacts_by_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)
    results = book.find_contacts_by_group(normalized_group)

    if not results:
        return f"No contacts found in group '{normalized_group}'."

    return results.to_table()

# GROUPS
@input_error
@require_args(1, "add-group <group>")
def add_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)
    book.add_group(normalized_group)
    return f"Group '{normalized_group}' added."


@input_error
@require_args(0, "all-groups")
def all_groups_command(args, book: AddressBook):
    groups = book.get_all_groups()

    if not groups:
        return "No groups found."

    return "Available groups: " + ", ".join(groups)


@input_error
@require_args(1, "delete-group <group>")
def delete_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)

    while True:
        confirm = input(
            f"Are you sure you want to delete group '{normalized_group}' from the system and all contacts? (Y/N): "
        ).strip().lower()

        if confirm in ("y", "yes"):
            book.delete_group(normalized_group)
            return f"Group '{normalized_group}' deleted."

        if confirm in ("n", "no"):
            return "Delete canceled."

        print("Please enter Y or N.")


@input_error
@require_args(2, "add-contact-group <contact_id> <group>")
def add_contact_group_command(args, book: AddressBook):
    record_id, group = args
    normalized_group = book.normalize_group_name(group)
    book.add_contact_to_group(record_id, normalized_group)
    return f"Contact ID [{record_id}] added to group '{normalized_group}'."


@input_error
@require_args(1, "add-contacts-to-group <group> <contact_id_1> <contact_id_2> ...")
def add_contacts_to_group_command(args, book: AddressBook):
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
    record_id, group = args
    normalized_group = book.normalize_group_name(group)
    book.delete_contact_group(record_id, normalized_group)
    return f"Contact ID [{record_id}] removed from group '{normalized_group}'."


@input_error
@require_args(1, "delete-contact-groups <contact_id>")
def delete_contact_groups_command(args, book: AddressBook):
    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return "Contact has no groups."

    record.clear_groups()
    return f"All groups removed from contact ID [{record_id}]."


@input_error
@require_args(1, "show-contact-groups <contact_id>")
def show_contact_groups_command(args, book: AddressBook):
    record_id = args[0]
    record = resolve_record(record_id, book, require_id_only=True)

    if not record.groups:
        return f"{record.name.value} has no groups."

    return f"{record.name.value}'s groups: {record.get_groups_display()}"


@input_error
@require_args(1, "search-contacts-by-group <group>")
def search_contacts_by_group_command(args, book: AddressBook):
    group = args[0]
    normalized_group = book.normalize_group_name(group)
    results = book.find_contacts_by_group(normalized_group)

    if not results:
        return f"No contacts found in group '{normalized_group}'."

    return results.to_table()


# SHOW ALL
@input_error
@require_args(0, "all")
def all_command(args, book: AddressBook):
    if not book or not book.data:
        return "No contacts found."

    return book.to_table(
        text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    )


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
@require_args(0, "add_note")
def add_note_command(args, notes_book: NotesBook):
    """
    Adds a note to NotesBook.
    If user provides no arguments, interactively ask for title and text.
    """
    tags = None

    if not args:
        title = input("Title (press Enter to skip): ").strip()
        tags = input("Tag (press Enter to skip): ").strip() or None
        text = input("Text: ").strip()

        if not text:
            raise ValueError("Note text cannot be empty.")
    else:
        title = args[0]
        text = " ".join(args[1:])
        if not text:
            text = input("Text: ").strip()
            if not text:
                raise ValueError("Note text cannot be empty.")

    note_id = notes_book.add_note(text=text, title=title, tags=tags)
    return f"Note '{title or 'Untitled'}' added successfully with ID [{note_id[:8]}]."


@input_error
@require_args(0, "show_notes")
def show_notes_command(args, notes_book: NotesBook):
    """
    Shows all notes with their IDs, titles, and text.
    """
    if not notes_book:
        return "No notes found."

    return notes_book.to_table()


@input_error
@require_args(1, "edit_note <id>")
def edit_note_command(args, notes_book: NotesBook):
    """
    Edits a note by its ID. Prompts user to update title and text.
    """
    note_id = args[0]
    note = notes_book.get_note_by_id(note_id)

    if note is None:
        raise ValueError(f"No note found with ID '{note_id}'.")

    print(f"Editing Note [ID: {note.id}]")
    print(f"Current Title: {note.title or 'Untitled'}")
    print(f"Current Text: {note.text}")

    new_title = input("New Title (leave empty to keep current): ").strip()
    new_text = input("New Text (leave empty to keep current): ").strip()

    final_title = new_title if new_title else note.title
    final_text = new_text if new_text else note.text

    if not final_text:
        raise ValueError("Text cannot be empty.")

    notes_book.edit_note_by_id(note_id, final_text, final_title)
    return f"Note [ID: {note_id}] updated successfully."


@input_error
@require_args(1, "delete_note <id>")
def delete_note_command(args, notes_book: NotesBook):
    """
    Deletes a note by its ID after confirmation.
    """
    note_id = args[0]

    note_to_delete = None
    for note in notes_book.data.values():
        if note.id == note_id:
            note_to_delete = note
            break

    if not note_to_delete:
        raise ValueError(f"No note found with ID '{note_id}'.")

    confirm = (
        input(
            f"Are you sure you want to delete note '{note_to_delete.title or 'Untitled'}'? (Y/N): "
        )
        .strip()
        .lower()
    )
    if confirm not in ("y", "yes"):
        return "Delete canceled."

    notes_book.delete_note_by_id(note_id)
    return f"Note '{note_to_delete.title or 'Untitled'}' deleted successfully."


@input_error
@require_args(1, "search_notes <keyword>")
def search_notes_command(args, notes_book: NotesBook):
    """
    Searches notes by ID, title, or text (partial matches allowed).
    """
    keyword = args[0].lower()

    results = notes_book.search_notes(keyword)

    if not results:
        return f"No notes found matching '{keyword}'."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(2, "add-tag <note_id> <tag>")
def add_tag_command(args, notes_book: NotesBook):
    """
    Adds a tag to a note by its ID.
    """
    note_id, tag = args[0], args[1]
    note = notes_book.get_note_by_id(note_id)
    note.add_tag(tag)
    return f"Tag '{tag}' added to note [ID: {note_id}]."


@input_error
@require_args(2, "remove-tag <note_id> <tag>")
def remove_tag_command(args, notes_book: NotesBook):
    """
    Removes a tag from a note by its ID.
    """
    note_id, tag = args[0], args[1]
    note = notes_book.get_note_by_id(note_id)
    note.remove_tag(tag)
    return f"Tag '{tag}' removed from note [ID: {note_id}]."


@input_error
@require_args(1, "show-tags <note_id>")
def show_tags_command(args, notes_book: NotesBook):
    """
    Shows all tags for a specific note.
    """
    note_id = args[0]
    note = notes_book.get_note_by_id(note_id)
    tags = getattr(note, "tags", set())

    if not tags:
        return f"Note [ID: {note_id}] has no tags."

    return f"Tags for note [ID: {note_id}]: {', '.join(sorted(tags))}"


@input_error
@require_args(1, "search-tag <tag>")
def search_tag_command(args, notes_book: NotesBook):
    """
    Searches notes by tag.
    """
    tag = args[0]
    results = notes_book.search_notes_by_tag(tag)

    if not results:
        return f"No notes found with tag '{tag}'."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(0, "sort-notes-by-tags")
def sort_notes_by_tags_command(args, notes_book: NotesBook):
    """
    Returns all notes sorted alphabetically by tags.
    """
    results = notes_book.sort_notes_by_tags()

    if not results:
        return "No notes found."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(0, "all-tags")
def all_tags_command(args, notes_book: NotesBook):
    """
    Shows all unique tags from all notes.
    """
    tags = notes_book.get_all_tags()

    if not tags:
        return "No tags found."

    return "Available tags: " + ", ".join(tags)
