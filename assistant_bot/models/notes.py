from collections import UserDict, UserList
from datetime import datetime
from assistant_bot.utils.colors import AnsiColor, table_cell_colored_value
from tabulate import tabulate


class Note:
    """Class representing a single note."""

    _id_counter = 1  # class-level counter

    def __init__(self, text, title=None, note_id=None, tags=None):
        if note_id is None:
            self.id = str(Note._id_counter)
            Note._id_counter += 1
        else:
            self.id = str(note_id)
            Note._id_counter = max(Note._id_counter, int(note_id) + 1)

        self.title = title or "Untitled"
        self.text = text

        if isinstance(tags, str):
            tags = [tags]

        self.tags = {tag.strip().lower() for tag in (tags or []) if tag.strip()}
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def add_tag(self, tag):
        """Add a tag to the note."""
        cleaned_tag = tag.strip().lower()
        if not cleaned_tag:
            raise ValueError("Tag cannot be empty.")
        self.tags.add(cleaned_tag)

    def remove_tag(self, tag):
        """Remove a tag from the note."""
        cleaned_tag = tag.strip().lower()
        if cleaned_tag not in self.tags:
            raise ValueError(f"Tag '{cleaned_tag}' not found.")
        self.tags.remove(cleaned_tag)

    def has_tag(self, tag):
        """Check whether note contains the given tag."""
        return tag.strip().lower() in self.tags

    def __str__(self):
        """Return a nicely formatted string representation of the note."""
        tags_str = ", ".join(sorted(self.tags)) if self.tags else "No tags"
        return (
            f"Title: {self.title}, "
            f"Text: {self.text}, "
            f"Tags: {tags_str}, "
            f"Created: {self.created_at}"
        )

    def to_colored_dict(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """Return the note formatted as a colored dictionary for table display."""
        tags_str = ", ".join(sorted(self.tags)) if self.tags else "No tags"
        return {
            "id": table_cell_colored_value(self.id, text_color, border_color),
            "title": table_cell_colored_value(self.title, text_color, border_color),
            "text": table_cell_colored_value(self.text, text_color, border_color),
            "tags": table_cell_colored_value(tags_str, text_color, border_color),
            "created_at": table_cell_colored_value(
                self.created_at, text_color, border_color
            ),
        }

    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """Return the note formatted as a colored table."""
        return AnsiColor.wrap(
            tabulate(
                [self.to_colored_dict(text_color, border_color)],
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )


class NotesList(UserList):
    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """Return a string representation of notes formatted as a colored table."""
        if not self.data:
            return AnsiColor.wrap("No notes found.", text_color)

        return AnsiColor.wrap(
            tabulate(
                [note.to_colored_dict(text_color, border_color) for note in self.data],
                headers="keys",
                tablefmt="fancy_grid",
            ),
            border_color,
        )


class NotesBook(UserDict):
    """Manage multiple Note instances by their unique IDs."""

    def add_note(self, text, title=None, tags=None):
        """Add a new note with the given text, optional title, and optional tags."""
        if self.data:
            next_id = str(max(int(i) for i in self.data.keys()) + 1)
        else:
            next_id = "1"

        note = Note(text=text, title=title, note_id=next_id, tags=tags)
        self.data[note.id] = note
        return note.id

    def get_note_by_id(self, note_id):
        note = self.data.get(note_id)
        if not note:
            raise ValueError(f"No note found with ID {note_id}")
        return note

    def edit_note_by_id(self, note_id, new_text=None, new_title=None):
        """Find a note by ID and update its fields."""
        note = self.get_note_by_id(note_id)

        if new_title:
            note.title = new_title

        if new_text:
            note.text = new_text

    def delete_note_by_id(self, note_id):
        """Delete a note using its ID."""
        self.get_note_by_id(note_id)
        del self.data[note_id]

    def search_notes(self, keyword):
        """Return a list of notes where the keyword appears in title, text, or ID."""
        keyword_lower = keyword.lower()
        results = [
            note
            for note in self.data.values()
            if keyword_lower in note.text.lower()
            or (note.title and keyword_lower in note.title.lower())
            or keyword_lower in note.id
        ]
        return results

    def search_notes_by_tag(self, tag):
        """Return notes that contain the given tag."""
        cleaned_tag = tag.strip().lower()
        return [note for note in self.data.values() if cleaned_tag in note.tags]

    def sort_notes_by_tags(self):
        """Return notes sorted alphabetically by tags."""
        return sorted(
            self.data.values(),
            key=lambda note: sorted(note.tags)[0] if note.tags else "",
        )

    def get_all_tags(self):
        """Return all unique tags sorted alphabetically."""
        all_tags = set()
        for note in self.data.values():
            all_tags.update(note.tags)
        return sorted(all_tags)

    def iter_notes(self):
        for note in self.data.values():
            if not hasattr(note, "tags"):
                note.tags = set()  # fix old notes
            yield note

    def __str__(self):
        """Return all notes nicely formatted."""
        if not self.data:
            return "No notes found."

        return "\n".join(
            f"ID: {note.id}, "
            f"Title: {note.title or 'Untitled'}, "
            f"Text: {note.text}, "
            f"Tags: {', '.join(sorted(note.tags)) if note.tags else 'No tags'}, "
            f"Created: {note.created_at}"
            for note in self.data.values()
        )

    def to_colored_dict(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """Return a list of notes formatted as colored dictionaries for table display."""

        return [
            note.to_colored_dict(text_color, border_color)
            for note in self.data.values()
        ]

    def to_table(
        self, text_color=AnsiColor.BRIGHT_GREEN, border_color=AnsiColor.BRIGHT_CYAN
    ):
        """Return a string representation of notes formatted as a colored table."""
        if not self.data:
            return AnsiColor.wrap("No notes found.", text_color)

        notes_list = NotesList(self.data.values())
        return notes_list.to_table(text_color, border_color)
