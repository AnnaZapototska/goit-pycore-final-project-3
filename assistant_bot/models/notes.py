from collections import UserDict
from datetime import datetime


class Note:
    """Class representing a single note."""

    def __init__(self, text, title=None):
        self.title = title
        self.text = text
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Automatically set creation timestamp

    def __str__(self):
        """Return a nicely formatted string representation of the note."""
        return f"Title: {self.title}, Text: {self.text}, Created: {self.created_at}"


class NotesBook(UserDict):
    """Class to manage multiple Note instances."""

    def add_note(self, title, text):
        if title in self.data:
            raise ValueError("Note with this title already exists.")
        self.data[title] = Note(text, title=title)

    def edit_note(self, title, new_text):
        if title not in self.data:
            raise ValueError("Note not found.")
        self.data[title].text = new_text

    def delete_note(self, title):
        if title not in self.data:
            raise ValueError("Note not found.")
        del self.data[title]

    def search_notes(self, keyword):
        keyword_lower = keyword.lower()
        return [
            note for note in self.data.values()
            if keyword_lower in note.title.lower() or keyword_lower in note.text.lower()
        ]

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())
    

note1 = Note("Buy milk")  # Title defaults to "Untitled"
note2 = Note("Finish report", "Work")  # Title is "Work"

print(note1)
print(note2)