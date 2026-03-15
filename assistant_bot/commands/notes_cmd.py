from assistant_bot.utils.decorators import input_error, require_args
from assistant_bot.models.notes import NotesBook, NotesList
from assistant_bot.services.notes_service import NoteService


def add_note_command(args, notes_book: NotesBook):
    """
    Adds a note to NotesBook.
    If user provides no arguments, interactively ask for title and text.
    """
    tags = None
    service = NoteService(notes_book)

    if not args:
        title = input("Title (press Enter to skip): ").strip()
        tags = input("Tag (press Enter to skip): ").strip() or None
        text = input("Text: ").strip()

        if not text:
            raise ValueError("Note text cannot be empty.")
    else:
        title = args[0]
        text = " ".join(args[1:])
        if not text:
            text = input("Text: ").strip()
            if not text:
                raise ValueError("Note text cannot be empty.")

    note_id = service.add_note(text=text, title=title, tags=tags)

    return f"Note '{title or 'Untitled'}' added successfully with ID [{note_id[:8]}]."


@input_error
@require_args(0, "all-notes")
def show_notes_command(args, notes_book: NotesBook):
    """
    Shows all notes.
    """
    service = NoteService(notes_book)
    notes = service.get_all_notes()

    if not notes or not notes.data:
        return "No notes found."

    return notes.to_table()


@input_error
@require_args(1, "edit-note <id>")
def edit_note_command(args, notes_book: NotesBook):
    """
    Edits a note by its ID.
    """
    note_id = args[0]
    service = NoteService(notes_book)

    note = service.get_note(note_id)

    print(f"Editing Note [ID: {note.id}]")
    print(f"Current Title: {note.title or 'Untitled'}")
    print(f"Current Text: {note.text}")

    new_title = input("New Title (leave empty to keep current): ").strip()
    new_text = input("New Text (leave empty to keep current): ").strip()

    final_title = new_title if new_title else note.title
    final_text = new_text if new_text else note.text

    if not final_text:
        raise ValueError("Text cannot be empty.")

    service.edit_note(note_id, final_text, final_title)

    return f"Note [ID: {note_id}] updated successfully."


@input_error
@require_args(1, "delete-note <id>")
def delete_note_command(args, notes_book: NotesBook):
    """
    Deletes a note by its ID after confirmation.
    """
    note_id = args[0]
    service = NoteService(notes_book)

    note = service.get_note(note_id)

    confirm = (
        input(
            f"Are you sure you want to delete note '{note.title or 'Untitled'}'? (Y/N): "
        )
        .strip()
        .lower()
    )

    if confirm not in ("y", "yes"):
        return "Delete canceled."

    service.delete_note(note_id)

    return f"Note '{note.title or 'Untitled'}' deleted successfully."


@input_error
@require_args(1, "search-notes <keyword>")
def search_notes_command(args, notes_book: NotesBook):
    """
    Searches notes by keyword.
    """
    keyword = args[0].lower()
    service = NoteService(notes_book)

    results = service.search_notes(keyword)

    if not results:
        return f"No notes found matching '{keyword}'."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(2, "add-note-tag <note_id> <tag>")
def add_tag_command(args, notes_book: NotesBook):
    """
    Adds a tag to a note by its ID.
    """
    note_id, tag = args
    service = NoteService(notes_book)
    service.add_tag(note_id, tag)
    return f"Tag '{tag}' added to note [ID: {note_id}]."


@input_error
@require_args(2, "remove-note-tag <note_id> <tag>")
def remove_tag_command(args, notes_book: NotesBook):
    """
    Removes a tag from a note.
    """
    note_id, tag = args
    service = NoteService(notes_book)

    service.remove_tag(note_id, tag)

    return f"Tag '{tag}' removed from note [ID: {note_id}]."


@input_error
@require_args(1, "show-notes-tags <note_id>")
def show_tags_command(args, notes_book: NotesBook):
    """
    Shows all tags for a specific note.
    """
    note_id = args[0]
    service = NoteService(notes_book)

    note = service.get_note(note_id)
    tags = getattr(note, "tags", set())

    if not tags:
        return f"Note [ID: {note_id}] has no tags."

    return f"Tags for note [ID: {note_id}]: {', '.join(sorted(tags))}"


@input_error
@require_args(1, "search-notes-by-tag <tag>")
def search_tag_command(args, notes_book: NotesBook):
    """
    Searches notes by tag.
    """
    tag = args[0]
    service = NoteService(notes_book)

    results = service.search_notes_by_tag(tag)

    if not results:
        return f"No notes found with tag '{tag}'."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(0, "sort-notes-by-tags")
def sort_notes_by_tags_command(args, notes_book: NotesBook):
    """
    Returns notes sorted by tags.
    """
    service = NoteService(notes_book)

    results = service.sort_by_tags()

    if not results:
        return "No notes found."

    notes_list = NotesList(results)
    return notes_list.to_table()


@input_error
@require_args(0, "all-notes-tags")
def all_tags_command(args, notes_book: NotesBook):
    """
    Shows all unique tags.
    """
    service = NoteService(notes_book)

    tags = service.get_all_tags()

    if not tags:
        return "No tags found."

    return "Available tags: " + ", ".join(tags)