import pickle
from models.contacts import AddressBook


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            if not isinstance(book, AddressBook):
                raise ValueError("Stored data is not an address book.")
            return book
    except FileNotFoundError:
        return AddressBook()
