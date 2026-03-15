# tests/test_contacts_commands.py
import os
import sys
import pytest

# Add project root for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from models.contacts import AddressBook
from services.contacts_service import ContactService
import commands.contacts_cmd as contacts_cmd

# --------------------------
# Fixtures
# --------------------------

@pytest.fixture
def empty_book():
    book = AddressBook()
    service = ContactService(book)
    return book, service


# --------------------------
# CONTACT COMMANDS TESTS
# --------------------------

def test_add_contact(empty_book):
    book, service = empty_book
    result = contacts_cmd.add_contact_command(["Alice", "1234567890", "alice@test.com"], book)
    assert "Contact added" in result
    record = next(iter(book.iter_records()))
    assert record.name.value == "Alice"
    assert record.primary_phone.value == "1234567890"
    assert record.email.value == "alice@test.com"


def test_change_phone(empty_book):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Bob", "0987654321"], book)
    record = next(iter(book.iter_records()))
    contact_id = record.id

    result = contacts_cmd.change_command([contact_id, "1112223333"], book)
    assert "Primary phone updated" in result
    updated_record = next(iter(book.iter_records()))
    assert updated_record.primary_phone.value == "1112223333"


def test_change_email(empty_book):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Charlie", "2223334444", "charlie@test.com"], book)
    record = next(iter(book.iter_records()))
    contact_id = record.id

    result = contacts_cmd.change_email_command([contact_id, "newcharlie@test.com"], book)
    assert result == "Email updated."
    updated_record = next(iter(book.iter_records()))
    assert updated_record.email.value == "newcharlie@test.com"


def test_edit_contact(empty_book):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Diana", "5551234567", "diana@test.com"], book)
    record = next(iter(book.iter_records()))

    result = contacts_cmd.edit_command([record.id, "email", "newdiana@test.com"], book)
    assert result == "Email updated."
    updated_record = next(iter(book.iter_records()))
    assert updated_record.email.value == "newdiana@test.com"


def test_add_show_birthday(empty_book):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Eve", "3334445555"], book)
    record = next(iter(book.iter_records()))
    contact_id = record.id

    contacts_cmd.add_birthday_command([contact_id, "01.01.2000"], book)
    result = contacts_cmd.show_birthday_command([contact_id], book)
    assert "Eve's birthday is on 01.01.2000" in result


def test_add_edit_remove_address(empty_book, monkeypatch):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Grace", "4445556666"], book)
    record = next(iter(book.iter_records()))
    contact_id = record.id

    # Add address
    inputs = iter(["123 Street", "New York", "USA"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = contacts_cmd.add_address_command([contact_id], book)
    assert result == "Address added."
    assert record.get_address() == "123 Street, New York, USA"

    # Edit address
    inputs2 = iter(["456 Avenue", "Boston", "USA"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs2))
    result = contacts_cmd.edit_address_command([contact_id], book)
    assert result == "Address updated."
    assert record.get_address() == "456 Avenue, Boston, USA"

    # Remove address
    result = contacts_cmd.remove_address_command([contact_id], book)
    assert result == "Address removed."
    assert record.get_address() == "no address"


def test_phone_and_all_commands(empty_book):
    book, service = empty_book
    contacts_cmd.add_contact_command(["John", "5555555555"], book)
    record = next(iter(book.iter_records()))
    contact_id = record.id

    result = contacts_cmd.phone_command([contact_id], book)
    assert "John's primary phone number is 5555555555" in result

    result_all = contacts_cmd.all_command([], book)
    assert record.name.value in result_all
    assert record.id in result_all


def test_delete_contact(empty_book, monkeypatch):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Kate", "7778889999"], book)
    record = next(iter(book.iter_records()))

    monkeypatch.setattr("builtins.input", lambda _: "y")
    result = contacts_cmd.delete_contact_command([record.id], book)
    assert result == "Contact deleted."
    assert record.id not in book.data


def test_delete_contact_cancel(empty_book, monkeypatch):
    book, service = empty_book
    contacts_cmd.add_contact_command(["Liam", "1231231234"], book)
    record = next(iter(book.iter_records()))

    monkeypatch.setattr("builtins.input", lambda _: "n")
    result = contacts_cmd.delete_contact_command([record.id], book)
    assert result == "Delete canceled."
    assert record.id in book.data


def test_delete_contact_missing(empty_book):
    book, service = empty_book
    result = contacts_cmd.delete_contact_command(["999"], book)
    assert result == "Contact ID 999 not found"