import pickle
from assistant_bot.models.contacts import AddressBook
from assistant_bot.models.notes import NotesBook


CONTACTS_FILE = "addressbook.pkl"
NOTES_FILE = "notes.pkl"


def save_data_contacts(book: AddressBook, filename: str = CONTACTS_FILE) -> None:
    """Save AddressBook to file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data_contacts(filename: str = CONTACTS_FILE) -> AddressBook:
    """Load AddressBook from file."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            if not isinstance(book, AddressBook):
                raise ValueError("Stored data is not an AddressBook.")
            return book
    except FileNotFoundError:
        return AddressBook()


def save_data_notes(notes_book: NotesBook, filename: str = NOTES_FILE) -> None:
    """Save NotesBook to file."""
    with open(filename, "wb") as f:
        pickle.dump(notes_book, f)


def load_data_notes(filename: str = NOTES_FILE) -> NotesBook:
    """Load NotesBook from file."""
    try:
        with open(filename, "rb") as f:
            notes = pickle.load(f)
            if not isinstance(notes, NotesBook):
                raise ValueError("Stored data is not a NotesBook.")
            return notes
    except FileNotFoundError:
        return NotesBook()
