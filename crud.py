
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas import UserCreate, NoteCreate

# Create a new user with existence check
def create_user(db: Session, user: UserCreate):
    existing = db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    db.execute(
        text("INSERT INTO users (username, email) VALUES (:username, :email)"),
        {"username": user.username, "email": user.email}
    )
    db.commit()

    user_result = db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": user.username}
    ).fetchone()
    return dict(user_result._mapping)

# Create a note for an existing user
def create_note(db: Session, note: NoteCreate, user_id: int):
    user_exists = db.execute(
        text("SELECT id FROM users WHERE id = :user_id"),
        {"user_id": user_id}
    ).fetchone()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    db.execute(
        text("INSERT INTO notes (title, content, user_id) VALUES (:title, :content, :user_id)"),
        {"title": note.title, "content": note.content, "user_id": user_id}
    )
    db.commit()

    inserted_note = db.execute(
        text("SELECT * FROM notes WHERE user_id = :user_id ORDER BY id DESC LIMIT 1"),
        {"user_id": user_id}
    ).fetchone()
    return dict(inserted_note._mapping)

# Retrieve all notes for a user
def get_notes_for_user(db: Session, user_id: int):
    notes = db.execute(
        text("SELECT * FROM notes WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchall()
    return [dict(note._mapping) for note in notes]

# Delete a note
def delete_note(db: Session, note_id: int, user_id: int):
    existing_note = db.execute(
        text("SELECT id FROM notes WHERE id = :note_id AND user_id = :user_id"),
        {"note_id": note_id, "user_id": user_id}
    ).fetchone()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.execute(
        text("DELETE FROM notes WHERE id = :note_id AND user_id = :user_id"),
        {"note_id": note_id, "user_id": user_id}
    )
    db.commit()
    return {"detail": "Note deleted successfully"}

# Update a note
def update_note(db: Session, note_id: int, user_id: int, updated_data: NoteCreate):
    existing_note = db.execute(
        text("SELECT * FROM notes WHERE id = :note_id AND user_id = :user_id"),
        {"note_id": note_id, "user_id": user_id}
    ).fetchone()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.execute(
        text("UPDATE notes SET title = :title, content = :content WHERE id = :note_id AND user_id = :user_id"),
        {
            "title": updated_data.title,
            "content": updated_data.content,
            "note_id": note_id,
            "user_id": user_id
        }
    )
    db.commit()

    updated_note = db.execute(
        text("SELECT * FROM notes WHERE id = :note_id"),
        {"note_id": note_id}
    ).fetchone()
    return dict(updated_note._mapping)


def get_user_by_username(username: str, db: Session):
    print(username)
    result = db.execute(
        text("SELECT id, username, email FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dict(result._mapping)

