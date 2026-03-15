from assistant_bot.models.notes import NotesBook


class NoteService:
    def __init__(self, notes_book: NotesBook):
        self.notes_book = notes_book

    # --- CREATE ---
    def add_note(self, text, title=None, tags=None):
        return self.notes_book.add_note(text=text, title=title, tags=tags)

    # --- READ ---
    def get_all_notes(self):
        return self.notes_book

    def get_note(self, note_id):
        note = self.notes_book.get_note_by_id(note_id)
        if note is None:
            raise ValueError(f"No note found with ID '{note_id}'.")
        return note

    # --- UPDATE ---
    def edit_note(self, note_id, text, title=None):
        self.get_note(note_id)
        self.notes_book.edit_note_by_id(note_id, text, title)

    # --- DELETE ---
    def delete_note(self, note_id):
        note = self.get_note(note_id)
        self.notes_book.delete_note_by_id(note_id)
        return note

    # --- SEARCH ---
    def search_notes(self, keyword):
        return self.notes_book.search_notes(keyword)

    def search_notes_by_tag(self, tag):
        return self.notes_book.search_notes_by_tag(tag)

    # --- TAGS ---
    def add_tag(self, note_id, tag):
        note = self.get_note(note_id)
        note.add_tag(tag)

    def remove_tag(self, note_id, tag):
        note = self.get_note(note_id)
        note.remove_tag(tag)

    def get_all_tags(self):
        return self.notes_book.get_all_tags()

    def sort_by_tags(self):
        return self.notes_book.sort_notes_by_tags()
