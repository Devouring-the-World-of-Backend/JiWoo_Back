from fastapi import APIRouter, HTTPException, Depends
from db.database import SessionLocal
from db.models import Book, User
from schemas import book, user
import user_crud

ur = APIRouter(
    prefix="/library"
)

# Create
@ur.post("/users")
def create_user(user: user.UserCreate):
    db = SessionLocal()
    user_data = user_crud.create_user(db=db, user=user)
    db.close()
    return user_data
# Active State
@ur.post("/users/{user_id}")
def active_user(user: user.UserBase):
    db = SessionLocal()
