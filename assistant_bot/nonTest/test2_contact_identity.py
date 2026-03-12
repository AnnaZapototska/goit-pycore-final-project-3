import os
import tempfile
import unittest

from bot import (
    add_birthday,
    add_contact,
    all_command,
    change_command,
    change_email_command,
    phone_command,
    show_birthday
)
from models.contacts import AddressBook, Record
from storage import load_data, save_data


class ContactIdentityTests(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_can_add_two_contacts_with_same_name_and_different_primary_phones(
            self):
        first_result = add_contact(
            ["Alice", "0123456789", "alice.one@example.com"], self.book)
        second_result = add_contact(
            ["Alice", "1234567890", "alice.two@example.com"], self.book)

        self.assertEqual(first_result, "Contact added.")
        self.assertEqual(second_result, "Contact added.")
        self.assertEqual(len(list(self.book.iter_records())), 2)
        self.assertEqual(
            self.book.find("0123456789").email.value,
            "alice.one@example.com")
        self.assertEqual(
            self.book.find("1234567890").email.value,
            "alice.two@example.com")

    def test_duplicate_primary_phone_is_treated_as_same_contact_update(self):
        add_contact(["Alice", "0123456789", "alice@example.com"], self.book)

        result = add_contact(["Alice Updated", "0123456789"], self.book)

        self.assertEqual(result, "Contact updated.")
        self.assertEqual(
            self.book.find("0123456789").name.value,
            "Alice Updated")
        self.assertEqual(len(list(self.book.iter_records())), 1)

    def test_duplicate_email_is_rejected(self):
        add_contact(["Alice", "0123456789", "shared@example.com"], self.book)

        result = add_contact(
            ["Bob", "1234567890", "shared@example.com"], self.book)

        self.assertEqual(result, "Email must be unique.")
        self.assertIsNone(self.book.find("1234567890"))

    def test_all_shows_contacts_with_same_name_as_separate_records(self):
        add_contact(
            ["Alice", "0123456789", "alice.one@example.com"], self.book)
        add_contact(
            ["Alice", "1234567890", "alice.two@example.com"], self.book)

        result = all_command([], self.book)

        self.assertIn("Contact name: Alice, primary phone: 0123456789", result)
        self.assertIn("Contact name: Alice, primary phone: 1234567890", result)

    def test_change_email_uses_phone_selector(self):
        add_contact(["Alice", "0123456789"], self.book)
        add_contact(["Alice", "1234567890"], self.book)

        result = change_email_command(
            ["1234567890", "alice.two@example.com"], self.book)

        self.assertEqual(result, "Email updated.")
        self.assertIsNone(self.book.find("0123456789").email)
        self.assertEqual(
            self.book.find("1234567890").email.value,
            "alice.two@example.com")

    def test_phone_and_birthday_commands_use_phone_or_email_selector(self):
        add_contact(["Alice", "0123456789", "alice@example.com"], self.book)

        birthday_result = add_birthday(
            ["alice@example.com", "01.01.2000"], self.book)
        phone_result = phone_command(["alice@example.com"], self.book)
        show_birthday_result = show_birthday(["0123456789"], self.book)

        self.assertEqual(birthday_result, "Birthday added.")
        self.assertEqual(
            phone_result,
            "Alice's primary phone number is 0123456789.")
        self.assertEqual(
            show_birthday_result,
            "Alice's birthday is on 2000-01-01.")

    def test_change_updates_primary_phone(self):
        add_contact(["Alice", "0123456789", "alice@example.com"], self.book)

        result = change_command(["alice@example.com", "1234567890"], self.book)

        self.assertEqual(result, "Primary phone updated.")
        self.assertIsNone(self.book.find("0123456789"))
        self.assertEqual(
            self.book.find("1234567890").email.value,
            "alice@example.com")

    def test_legacy_storage_is_migrated_to_primary_phone_keys(self):
        legacy_book = AddressBook()
        legacy_record = Record("Legacy Alice", "0123456789")
        legacy_record.add_phone("1234567890")
        legacy_record.add_email("legacy@example.com")
        legacy_book.data = {"Legacy Alice": legacy_record}

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            filename = tmp_file.name

        try:
            save_data(legacy_book, filename)
            loaded_book = load_data(filename)
        finally:
            os.remove(filename)

        loaded_record = loaded_book.find("0123456789")
        self.assertIsNotNone(loaded_record)
        self.assertEqual(loaded_record.name.value, "Legacy Alice")
        self.assertEqual(loaded_record.primary_phone.value, "0123456789")
        self.assertEqual(loaded_record.phones[1].value, "1234567890")
        self.assertEqual(loaded_record.email.value, "legacy@example.com")


if __name__ == "__main__":
    unittest.main()
