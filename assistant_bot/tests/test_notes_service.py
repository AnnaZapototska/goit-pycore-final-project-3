# tests/test_contacts_commands.py
import os
import sys
import pytest

# Add project root for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from assistant_bot.models.notes import NotesBook
from assistant_bot.services.notes_service import NoteService
import assistant_bot.commands.notes_cmd as notes_cmd

# --------------------------
# Fixtures
# --------------------------
@pytest.fixture
def empty_notes_book():
    notes_book = NotesBook()
    service = NoteService(notes_book)
    return notes_book, service


# --------------------------
# NOTES COMMANDS TESTS
# --------------------------

def test_add_note_with_args(empty_notes_book):
    notes_book, service = empty_notes_book
    result = notes_cmd.add_note_command(["MyNote", "This is note text"], notes_book)
    assert "Note 'MyNote' added successfully" in result
    note = next(iter(notes_book.data.values()))
    assert note.title == "MyNote"
    assert note.text == "This is note text"


def test_add_note_interactive(empty_notes_book, monkeypatch):
    notes_book, service = empty_notes_book
    inputs = iter(["InteractiveNote", "tag1", "Some interactive text"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = notes_cmd.add_note_command([], notes_book)
    assert "Note 'InteractiveNote' added successfully" in result
    note = next(iter(notes_book.data.values()))
    assert note.title == "InteractiveNote"
    assert note.text == "Some interactive text"
    assert "tag1" in note.tags


def test_show_notes(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["Note1", "Text1"], notes_book)
    notes_cmd.add_note_command(["Note2", "Text2"], notes_book)
    result = notes_cmd.show_notes_command([], notes_book)
    assert "Note1" in result
    assert "Note2" in result


def test_edit_note_command(empty_notes_book, monkeypatch):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["EditMe", "Original text"], notes_book)
    note = next(iter(notes_book.data.values()))
    note_id = note.id

    inputs = iter(["EditedTitle", "Edited text"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = notes_cmd.edit_note_command([note_id], notes_book)

    assert f"Note [ID: {note_id}] updated successfully." == result
    updated_note = next(iter(notes_book.data.values()))
    assert updated_note.title == "EditedTitle"
    assert updated_note.text == "Edited text"


def test_delete_note_confirmed(empty_notes_book, monkeypatch):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["DeleteMe", "To be deleted"], notes_book)
    note = next(iter(notes_book.data.values()))
    note_id = note.id

    monkeypatch.setattr("builtins.input", lambda _: "y")
    result = notes_cmd.delete_note_command([note_id], notes_book)
    assert f"Note '{note.title}' deleted successfully." == result
    assert note_id not in notes_book.data


def test_delete_note_cancel(empty_notes_book, monkeypatch):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["KeepMe", "Do not delete"], notes_book)
    note = next(iter(notes_book.data.values()))
    note_id = note.id

    monkeypatch.setattr("builtins.input", lambda _: "n")
    result = notes_cmd.delete_note_command([note_id], notes_book)
    assert result == "Delete canceled."
    assert note_id in notes_book.data


def test_search_notes(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["FirstNote", "Text alpha"], notes_book)
    notes_cmd.add_note_command(["SecondNote", "Text beta"], notes_book)

    result = notes_cmd.search_notes_command(["alpha"], notes_book)
    assert "FirstNote" in result
    assert "SecondNote" not in result


def test_tag_management(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["TaggedNote", "Some text"], notes_book)
    note = next(iter(notes_book.data.values()))
    note_id = note.id

    # Add tag
    result = notes_cmd.add_tag_command([note_id, "urgent"], notes_book)
    assert "Tag 'urgent' added" in result
    assert "urgent" in note.tags

    # Show tags
    result_show = notes_cmd.show_tags_command([note_id], notes_book)
    assert "urgent" in result_show

    # Remove tag
    result_remove = notes_cmd.remove_tag_command([note_id, "urgent"], notes_book)
    assert "Tag 'urgent' removed" in result_remove
    assert "urgent" not in note.tags


def test_search_notes_by_tag(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["NoteA", "Text"], notes_book)
    notes_cmd.add_note_command(["NoteB", "Text"], notes_book)
    note_ids = list(notes_book.data.keys())
    notes_cmd.add_tag_command([note_ids[0], "tag1"], notes_book)
    notes_cmd.add_tag_command([note_ids[1], "tag2"], notes_book)

    result_tag1 = notes_cmd.search_tag_command(["tag1"], notes_book)
    assert "NoteA" in result_tag1
    assert "NoteB" not in result_tag1


def test_all_tags_command(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["NoteX", "Text"], notes_book)
    note_id = next(iter(notes_book.data.keys()))
    notes_cmd.add_tag_command([note_id, "tagX"], notes_book)

    result = notes_cmd.all_tags_command([], notes_book)
    assert "tagx" in result.lower()  


def test_sort_notes_by_tags_command(empty_notes_book):
    notes_book, service = empty_notes_book
    notes_cmd.add_note_command(["Note1", "Text1"], notes_book)
    notes_cmd.add_note_command(["Note2", "Text2"], notes_book)
    note_ids = list(notes_book.data.keys())
    notes_cmd.add_tag_command([note_ids[0], "aaa"], notes_book)
    notes_cmd.add_tag_command([note_ids[1], "bbb"], notes_book)

    result = notes_cmd.sort_notes_by_tags_command([], notes_book)
    assert "Note1" in result and "Note2" in result