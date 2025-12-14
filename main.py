from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi import Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

import crud
import models
import schemas
from database import SessionLocal, engine

client = OpenAI()

def generate_ai_summary(query: str) -> str:
    """
    Generates a one-paragraph summary using GPT-4o based on the user query.
    """
    prompt = (
        "Write a clear, single-paragraph note about the following topic. "
        "Make it concise but informative:\n\n" + query
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You write high-quality notes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()



API_KEY = "supersecretkey123"  # Change in production!
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return crud.create_user(db=db, user=user)


@app.post("/users/{user_id}/notes/", response_model=schemas.NoteOut)
def create_note_for_user(
    user_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return crud.create_note(db=db, note=note, user_id=user_id)


@app.get("/users/{user_id}/notes/", response_model=list[schemas.NoteOut])
def read_notes(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return crud.get_notes_for_user(db, user_id)


@app.put("/users/{user_id}/notes/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    user_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    updated_note = crud.update_note(db, note_id, user_id, note)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@app.delete("/users/{user_id}/notes/{note_id}")
def delete_note(
    note_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    success = crud.delete_note(db, note_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted successfully"}


@app.get("/users/by-username/{username}", response_model=schemas.UserOut)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return crud.get_user_by_username(username, db)

@app.post("/users/{user_id}/notes/ai-summary", response_model=schemas.NoteOut)
def create_ai_summary_note(
    user_id: int,
    query: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    summary = generate_ai_summary(query)

    note_data = schemas.NoteCreate(
        title="AI Summary",
        content=summary
    )

    return crud.create_note(db, note_data, user_id)

