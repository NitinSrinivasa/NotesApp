from pydantic import BaseModel
from typing import Optional

# Schema for creating a new user (incoming request)
class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None  # optional field

# Schema for creating a new note (incoming request)
class NoteCreate(BaseModel):
    title: str
    content: str

from typing import List

# What we return when we fetch a note
class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True

# What we return when we fetch a user (with notes)
class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
   

    class Config:
        orm_mode = True
