from fastapi import APIRouter, HTTPException, Depends
from db.database import Session
from db.models import Book, User
from schemas import book, user
import user_crud

ur = APIRouter(
    prefix="/library"
)

# Create
@ur.post("/users")
async def create_user(user: user.UserCreate):
    db = Session()
    user_data = user_crud.create_user(db=db, user=user)
    db.close()
    return user_data
# Active State
@ur.post("/users/{user_id}")
async def active_user(user: user.UserBase):
    db = Session()
