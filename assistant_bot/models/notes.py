from collections import UserDict
from datetime import datetime

class Note:
    """Class representing a single note."""
    _id_counter = 1  # class-level counter

    def __init__(self, text, title=None, note_id=None):
        if note_id is None:
            self.id = str(Note._id_counter)
            Note._id_counter += 1
        else:
            self.id = str(note_id)
            Note._id_counter = max(Note._id_counter, int(note_id) + 1)
        self.title = title or "Untitled"
        self.text = text
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S") # Automatically set creation timestamp

    def __str__(self):
        """Return a nicely formatted string representation of the note."""
        return f"Title: {self.title}, Text: {self.text}, Created: {self.created_at}"


class NotesBook(UserDict):
    """Manage multiple Note instances by their unique IDs."""

    def add_note(self, text, title=None):
        """Add a new note with the given text and optional title. Automatically assigns a unique ID."""
        if self.data:
            next_id = str(max(int(i) for i in self.data.keys()) + 1)
        else:
            next_id = "1"
        note = Note(text=text, title=title, note_id=next_id)
        self.data[note.id] = note
        return note.id
    
    def get_note_by_id(self, note_id):
        note = self.data.get(note_id)
        if not note:
            raise ValueError(f"No note found with ID {note_id}")
        return note

    def edit_note_by_id(self, note_id, new_text=None, new_title=None):
        """
        Find a note by ID and update its text.
        """
        note = self.get_note_by_id(note_id)
        if new_title:
            note.title = new_title

        if new_text:
            note.text = new_text


    def delete_note_by_id(self, note_id):
        """
        Delete a note using its ID.
        """
        note = self.get_note_by_id(note_id)
        del self.data[note_id]

    def search_notes(self, keyword):
        """Return a list of notes where the keyword appears in title or text."""
        keyword_lower = keyword.lower()
        return [
            note for note in self.data.values()
            if keyword_lower in note.text.lower()
            or (note.title and keyword_lower in note.title.lower())
            or keyword_lower in note.id
        ]

    def iter_notes(self):
        """Yield all Note objects in the book."""
        return self.data.values()
    
    def __str__(self):
        """Return all notes nicely formatted."""
        if not self.data:
            return "No notes found."
        return "\n".join(
            f"ID: {note.id}, Title: {note.title or 'Untitled'}, Text: {note.text}, Created: {note.created_at}"
            for note in self.data.values()
        )