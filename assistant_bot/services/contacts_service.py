from assistant_bot.models.contacts import AddressBook, Record
from assistant_bot.models.fields import Phone, Email


class ContactService:
    def __init__(self, book: AddressBook):
        self.book = book

    # --- CONTACTS ---

    def add_contact(self, name: str, phone: str, email=None):
        """Adds a new contact with the provided name, phone, and optional email."""
        validated_phone = Phone(phone)
        self.book.ensure_phone_unique(validated_phone.value)

        record = Record(name, validated_phone.value)

        if email:
            validated_email = Email(email)
            self.book.ensure_email_unique(validated_email.value)
            record.add_email(validated_email.value)

        self.book.add_record(record)
        return record
    
    def search(self, query: str):
        """Searches for contacts matching the query in name, phone, or email."""
        return self.book.search(query)

    def change_primary_phone(self, record_id: str, new_phone: str):
        """Changes the primary phone number for a contact."""
        self.book.replace_primary_phone(record_id, new_phone)


    def change_email(self, record, new_email: str):
        """Edits the contact's email."""
        validated_email = Email(new_email)
        self.book.ensure_email_unique(validated_email.value, record.id)

        if record.email is None:
            record.add_email(validated_email.value)
        else:
            record.edit_email(validated_email.value)


    def edit_phone(self, record, old_phone: str, new_phone: str):
        """Edits a specific phone number for a contact."""
        validated_new_phone = Phone(new_phone)
        self.book.ensure_phone_unique(validated_new_phone.value, owner_record_id=record.id)

        record.edit_phone(old_phone, validated_new_phone.value)


    def delete_contact(self, record_id: str):
        """Deletes a contact by its ID."""
        self.book.delete(record_id)

    # --- ADDRESS ---

    def add_address(self, record, full_address: str):
        """Adds an address to the contact."""
        record.add_address(full_address)

    def edit_address(self, record, full_address: str):
        """Edits the contact's address."""
        record.edit_address(full_address)

    def remove_address(self, record):
        """Removes the contact's address."""
        record.remove_address()

    def get_address(self, record):
        """Returns the contact's address or a message if not set."""
        return record.get_address()

    # --- GROUPS ---

    def add_group(self, group: str):
        """Adds a new group."""
        normalized_group = self.book.normalize_group_name(group)
        self.book.add_group(normalized_group)
        return normalized_group


    def delete_group(self, group: str):
        """Deletes a group and removes all contacts from it."""
        normalized_group = self.book.normalize_group_name(group)
        self.book.delete_group(normalized_group)
        return normalized_group


    def add_contact_to_group(self, record_id: str, group: str):
        """Adds a contact to a group."""
        normalized_group = self.book.normalize_group_name(group)
        self.book.add_contact_to_group(record_id, normalized_group)
        return normalized_group


    def add_contacts_to_group(self, group: str, record_ids):
        """Adds multiple contacts to a group."""
        return self.book.add_contacts_to_group(group, record_ids)

    def remove_contact_from_group(self, record_id: str, group: str):
        """Removes a contact from a group."""
        normalized_group = self.book.normalize_group_name(group)
        self.book.delete_contact_group(record_id, normalized_group)
        return normalized_group
    # --- GROUPS HELPERS ---

    def clear_contact_groups(self, record):
        """
        Removes all groups from a contact.
        """
        record.clear_groups()

    def get_contact_groups(self, record):
        """
        Returns a list of groups a contact belongs to.
        """
        return record.get_groups_display()

    def find_contacts_by_group(self, group: str):
        """
        Returns all contacts in the specified group.
        """
        normalized_group = self.book.normalize_group_name(group)
        return self.book.find_contacts_by_group(normalized_group)
    
    # --- BIRTHDAY ---

    def add_birthday(self, record, birthday: str):
        """Adds or updates the birthday for a contact."""
        record.add_birthday(birthday)

    def get_upcoming_birthdays(self, days_ahead: int):
        """Returns a list of contacts with birthdays in the next specified number of days."""
        return self.book.get_upcoming_birthdays(days_ahead=days_ahead)