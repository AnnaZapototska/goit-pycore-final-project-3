import pickle
from models.contacts import AddressBook
from models.notes import NotesBook


CONTACTS_FILE = "addressbook.pkl"
NOTES_FILE = "notes.pkl"


def save_data_contacts(book, filename=CONTACTS_FILE):
    """Save AddressBook to file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data_contacts(filename=CONTACTS_FILE):
    """Load AddressBook from file."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            if not isinstance(book, AddressBook):
                raise ValueError("Stored data is not an AddressBook.")
            return book
    except FileNotFoundError:
        return AddressBook()


def save_data_notes(notes_book, filename=NOTES_FILE):
    """Save NotesBook to file."""
    with open(filename, "wb") as f:
        pickle.dump(notes_book, f)


def load_data_notes(filename=NOTES_FILE):
    """Load NotesBook from file."""
    try:
        with open(filename, "rb") as f:
            notes = pickle.load(f)
            if not isinstance(notes, NotesBook):
                raise ValueError("Stored data is not a NotesBook.")
            return notes
    except FileNotFoundError:
        return NotesBook()