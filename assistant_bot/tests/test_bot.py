import os
import sys
import pytest

# # Add the assistant_bot folder to sys.path so imports in bot.py work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Now bot.py imports will resolve correctly
from bot import (
    add_contact_command,
    change_command,
    change_email_command,
    delete_contact_command,
    phone_command,
    add_birthday_command,
    show_birthday_command,
    add_address_command,
    edit_address_command,
    remove_address_command,
    all_command,
    hello_command,
    help_command,
    add_note_command,
    show_notes_command,
    edit_note_command,
    delete_note_command,
    search_notes_command,
)
from models.contacts import AddressBook
from models.notes import NotesBook, Note
from utils.help_view import build_welcome_message

# --------------------------
# Fixtures
# --------------------------


@pytest.fixture
def empty_book():
    return AddressBook()


@pytest.fixture
def notes_book():
    return NotesBook()


# --------------------------
# TESTS
# --------------------------


def test_hello_command(empty_book):
    result = hello_command([], empty_book)
    assert result == "How can I help you?"


# -------------------------
# TEST WELCOME MESSAGE
# -------------------------
def test_welcome_message_contains_drevo_and_hint():
    result = build_welcome_message()
    assert "█████╗" in result
    assert "PERSONAL ASSISTANT BOT" in result
    assert "Contacts • Notes" in result
    assert 'Type "help" to see commands' in result


# -------------------------
# TEST HELP COMMAND
# -------------------------
def test_help_command_contains_grouped_tables(empty_book):
    result = help_command([], empty_book)
    assert "Global" in result
    assert "Contacts" in result
    assert "Notes" in result
    assert "Tags" in result
    assert "Command" in result
    assert "Description" in result
    assert "Example" in result
    assert "Show all contacts" in result
    assert "Add a new contact" in result
    assert "Create a new note" in result
    assert "Add a tag to a note" in result
    assert "all-contacts" in result
    assert "add-contact" in result
    assert "add-note" in result
    assert "add-note-tag" in result


# -------------------------
# TEST ADD CONTACT
# -------------------------
def test_add_contact(empty_book):
    result = add_contact_command(["Alice", "1234567890", "alice@test.com"], empty_book)
    assert "Contact added" in result

    # Get the record
    record = next(iter(empty_book.iter_records()))
    assert record is not None
    assert record.name.value == "Alice"
    assert record.primary_phone.value == "1234567890"
    assert record.email.value == "alice@test.com"


# -------------------------
# TEST CHANGE PHONE
# -------------------------
def test_change_phone(empty_book):
    add_contact_command(["Bob", "0987654321"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    result = change_command([contact_id, "1112223333"], empty_book)
    assert "Primary phone updated" in result

    updated_record = next(iter(empty_book.iter_records()))
    assert updated_record.primary_phone.value == "1112223333"
    assert updated_record.name.value == "Bob"


# -------------------------
# TEST CHANGE EMAIL
# -------------------------
def test_change_email(empty_book):
    add_contact_command(["Charlie", "2223334444", "charlie@test.com"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    result = change_email_command([contact_id, "newcharlie@test.com"], empty_book)
    assert result == "Email updated."

    updated_record = next(iter(empty_book.iter_records()))
    assert updated_record.email.value == "newcharlie@test.com"


# -------------------------
# TEST ADD & SHOW BIRTHDAY
# -------------------------
def test_add_show_birthday(empty_book):
    add_contact_command(["Eve", "3334445555"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    add_birthday_command([contact_id, "01.01.2000"], empty_book)
    result = show_birthday_command([contact_id], empty_book)
    assert "Eve's birthday is on 01.01.2000" in result


# -------------------------
# TEST ADD & SHOW ADDRESS
# -------------------------
def test_add_show_address(empty_book, monkeypatch):
    add_contact_command(["Grace", "4445556666"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    # Mock user input for address
    inputs = iter(["123 Street", "New York", "USA"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = add_address_command([contact_id], empty_book)
    assert result == "Address added."

    updated_record = next(iter(empty_book.iter_records()))
    assert updated_record.get_address() == "123 Street, New York, USA"


# -------------------------
# TEST EDIT ADDRESS
# -------------------------
def test_edit_address(empty_book, monkeypatch):
    add_contact_command(["Hank", "1112223333"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    # Add initial address
    inputs1 = iter(["Street A", "City A", "Country A"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs1))
    add_address_command([contact_id], empty_book)

    # Edit address
    inputs2 = iter(["Street B", "City B", "Country B"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs2))
    result = edit_address_command([contact_id], empty_book)
    assert result == "Address updated."

    updated_record = next(iter(empty_book.iter_records()))
    assert updated_record.get_address() == "Street B, City B, Country B"


# -------------------------
# TEST REMOVE ADDRESS
# -------------------------
def test_remove_address(empty_book, monkeypatch):
    add_contact_command(["Ivy", "9998887777"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    # Add address
    inputs = iter(["Street 1", "City 1", "Country 1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    add_address_command([contact_id], empty_book)

    # Remove address
    result = remove_address_command([contact_id], empty_book)
    assert result == "Address removed."

    updated_record = next(iter(empty_book.iter_records()))
    assert updated_record.get_address() == "no address"


# -------------------------
# TEST PHONE COMMAND
# -------------------------
def test_phone_command(empty_book):
    add_contact_command(["John", "5555555555"], empty_book)
    record = next(iter(empty_book.iter_records()))
    contact_id = record.id

    result = phone_command([contact_id], empty_book)
    assert "John's primary phone number is 5555555555" in result


# -------------------------
# TEST ALL COMMAND
# -------------------------
def test_all_command(empty_book):
    add_contact_command(["Alice", "1234567890"], empty_book)
    add_contact_command(["Bob", "0987654321"], empty_book)

    result = all_command([], empty_book)
    # Check names and IDs are present
    for record in empty_book.iter_records():
        assert record.name.value in result
        assert record.id in result


def test_delete_contact_by_id(empty_book, monkeypatch):
    add_contact_command(["Kate", "7778889999"], empty_book)
    record = next(iter(empty_book.iter_records()))

    monkeypatch.setattr("builtins.input", lambda _: "y")

    result = delete_contact_command([record.id], empty_book)
    assert result == "Contact deleted."
    assert record.id not in empty_book.data


def test_delete_contact_cancelled(empty_book, monkeypatch):
    add_contact_command(["Liam", "1231231234"], empty_book)
    record = next(iter(empty_book.iter_records()))

    monkeypatch.setattr("builtins.input", lambda _: "n")

    result = delete_contact_command([record.id], empty_book)
    assert result == "Delete canceled."
    assert record.id in empty_book.data


def test_delete_contact_missing_id(empty_book):
    result = delete_contact_command(["999"], empty_book)
    assert result == "Contact ID 999 not found"


def test_add_note_command(monkeypatch, notes_book):
    # Simulate user input for title and text interactively
    inputs = iter(["My Note", "", "This is the note text"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Call command with empty args to trigger interactive mode
    result = add_note_command([], notes_book)
    assert "added successfully" in result
    assert len(notes_book.data) == 1
    note = list(notes_book.data.values())[0]
    assert note.title == "My Note"
    assert note.text == "This is the note text"


def test_show_notes_command(notes_book):
    # Add notes directly
    note = Note("Some text", title="Test Note")
    notes_book.data[note.id] = note

    output = show_notes_command([], notes_book)
    assert "Test Note" in output
    assert "Some text" in output
    assert note.id in output


def test_edit_note_command(monkeypatch, notes_book):
    # Add a note
    note = Note("Old text", title="Old Title")
    notes_book.data[note.id] = note

    # Simulate interactive input for new title and text
    inputs = iter(["New Title", "Updated text"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Call command with just ID
    result = edit_note_command([note.id], notes_book)
    assert "updated successfully" in result
    updated_note = notes_book.get_note_by_id(note.id)
    assert updated_note.title == "New Title"
    assert updated_note.text == "Updated text"


def test_delete_note_command(monkeypatch, notes_book):
    # Add a note
    note = Note("Delete this note", title="ToDelete")
    notes_book.data[note.id] = note

    # Simulate confirmation 'y'
    monkeypatch.setattr("builtins.input", lambda _: "y")

    result = delete_note_command([note.id], notes_book)
    assert "deleted successfully" in result
    assert note.id not in notes_book.data


def test_search_notes_command(notes_book):
    note1 = Note("Buy milk", title="Shopping")
    note2 = Note("Finish report", title="Work")
    notes_book.data[note1.id] = note1
    notes_book.data[note2.id] = note2

    # Search by title
    result = search_notes_command(["Shop"], notes_book)
    assert "Shopping" in result

    # Search by text
    result = search_notes_command(["report"], notes_book)
    assert "Finish report" in result

    # Search by ID
    result = search_notes_command([note1.id], notes_book)
    assert "Buy milk" in result
