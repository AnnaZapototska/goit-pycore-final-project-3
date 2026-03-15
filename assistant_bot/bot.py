from models.contacts import AddressBook
from models.fields import Email, Phone, Address


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
            validated_email.value, owner_record_id=record.id
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


# --- notes commands ---

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




