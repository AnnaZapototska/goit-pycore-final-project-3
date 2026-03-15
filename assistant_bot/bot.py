from assistant_bot.models.contacts import AddressBook, Record
from assistant_bot.models.fields import Email, Phone, Address


def resolve_record(
    selector: str, book: AddressBook, require_id_only: bool = False
) -> Record:
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


def apply_contact_edit(
    record: Record, field: str, new_value: str, book: AddressBook
) -> str:
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
        book.ensure_email_unique(validated_email.value, owner_record_id=record.id)

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
