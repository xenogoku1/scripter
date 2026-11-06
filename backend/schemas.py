from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- AUTHENTICATION ---

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- SCRIPT STUFF ---

class ScriptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    content: str
    anime_title: Optional[str] = None

class ScriptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    anime_title: Optional[str] = None


# --- TRANSCRIPT / VOICE NOTES SCHEMAS ---

class AudioNoteCreate(BaseModel):
    script_id: Optional[str] = None  # Link to a script if applicable
    raw_transcript: str
    cleaned_transcript: Optional[str] = None