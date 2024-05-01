# Create the pydantic models
from typing import Optional
from pydantic import BaseModel, Field
from .book import Book

# Response Model
class UserBase(BaseModel):
    id: int
    name: str
    email: str

# Create user
class UserCreate(BaseModel):
    email: str
    password: str

# Update user
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str] = None
    
# Response Model
class User(BaseModel):
    id: int
    is_active: bool

    class Config:
        orm_mode=True