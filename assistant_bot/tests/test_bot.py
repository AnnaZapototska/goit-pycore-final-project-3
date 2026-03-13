import os
import sys
import pytest

# # Add the assistant_bot folder to sys.path so imports in bot.py work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Now bot.py imports will resolve correctly
from bot import (
    add_contact,
    change_command,
    change_email_command,
    phone_command,
    add_birthday,
    show_birthday,
    add_address_command,
    edit_address_command,
    remove_address_command,
    all_command,
    hello_command
)
from models.contacts import AddressBook

# --------------------------
# Fixtures
# --------------------------


@pytest.fixture
def empty_book():
    return AddressBook()

# --------------------------
# TESTS
# --------------------------


def test_hello_command(empty_book):
    result = hello_command([], empty_book)
    assert result == "How can I help you?"


def test_add_contact(empty_book):
    result = add_contact(["Alice", "1234567890", "alice@test.com"], empty_book)
    assert "Contact added" in result
    record = empty_book.find("1234567890")
    assert record is not None
    assert record.name.value == "Alice"
    assert record.primary_phone.value == "1234567890"
    assert record.email.value == "alice@test.com"


def test_change_phone(empty_book):
    add_contact(["Bob", "0987654321"], empty_book)
    result = change_command(["0987654321", "1112223333"], empty_book)
    assert "Primary phone updated" in result
    record = empty_book.find("1112223333")
    assert record.primary_phone.value == "1112223333"
    assert record.name.value == "Bob"


def test_change_email(empty_book):
    add_contact(["Charlie", "2223334444", "charlie@test.com"], empty_book)
    result = change_email_command(
        ["2223334444", "newcharlie@test.com"], empty_book)
    assert result == "Email updated."
    record = empty_book.find("2223334444")
    assert record.email.value == "newcharlie@test.com"


def test_add_show_birthday(empty_book):
    add_contact(["Eve", "3334445555"], empty_book)
    add_birthday(["3334445555", "01.01.2000"], empty_book)
    result = show_birthday(["3334445555"], empty_book)
    assert "Eve's birthday is on 01.01.2000." in result


def test_add_show_address(empty_book, monkeypatch):
    add_contact(["Grace", "4445556666"], empty_book)

    # Mock user input for address
    inputs = iter(["123 Street", "New York", "USA"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = add_address_command(["4445556666"], empty_book)
    assert result == "Address added."

    record = empty_book.find("4445556666")
    assert record.get_address() == "123 Street, New York, USA"


def test_edit_address(empty_book, monkeypatch):
    add_contact(["Hank", "1112223333"], empty_book)

    # Add initial address
    inputs1 = iter(["Street A", "City A", "Country A"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs1))
    add_address_command(["1112223333"], empty_book)

    # Edit address
    inputs2 = iter(["Street B", "City B", "Country B"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs2))
    result = edit_address_command(["1112223333"], empty_book)
    assert result == "Address updated."

    record = empty_book.find("1112223333")
    assert record.get_address() == "Street B, City B, Country B"


def test_remove_address(empty_book, monkeypatch):
    add_contact(["Ivy", "9998887777"], empty_book)

    # Add address
    inputs = iter(["Street 1", "City 1", "Country 1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_address_command(["9998887777"], empty_book)

    # Remove address
    result = remove_address_command(["9998887777"], empty_book)
    assert result.strip(".") == "Address removed"

    record = empty_book.find("9998887777")
    assert record.get_address() == "no address"


def test_phone_command(empty_book):
    add_contact(["John", "5555555555"], empty_book)
    result = phone_command(["5555555555"], empty_book)
    assert "John's primary phone number is 5555555555" in result


def test_all_command(empty_book):
    add_contact(["Alice", "1234567890"], empty_book)
    add_contact(["Bob", "0987654321"], empty_book)
    result = all_command([], empty_book)
    assert "Alice" in result
    assert "Bob" in result
