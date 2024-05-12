from fastapi import APIRouter, HTTPException, Depends
from db.database import SessionLocal, get_db
from db.models import Book
from sqlalchemy.orm import Session
from schemas import book
import book_crud
import contextlib

br = APIRouter(
    prefix="/library"
)

@br.get("/")
def root():
    return {"message":"Hello Library!"}

#Create
@br.post("/books", status_code=201, response_model=book.Book)
def create_book(book: book.BookCreate, db: Session = Depends(get_db)):
    print(type(db))
    data = book_crud.create_book(db=db, book=book)
    return data
# Read
@br.get("/books")
def get_books():
    db = Session()
    datas = book_crud.get_books(db=db)
    db.close()
    return datas

@br.get("/books/search", status_code = 201,response_model = book.BookSearch)
def search_book():
    db = Session()
    data = book_crud.search_book(db=db, book = book)
    db.close()
    return data
# Update
@br.put("/books/{book_id}", response_model = book.BookUpdate)
def update_book(id: int, book = book.Book):
    db = Session()
    data = book_crud.update_book(db=db, book = book, book_id = id)
    db.close()
    print("Update Succeed")
    return data
# Delete
@br.delete("/books/{book_id}")
def delete_book(id: int):
    db = Session()
    data = book_crud.delete_book(db = db, book_id = id)
    db.close()
    print("Deletion Succeed")
    return data
