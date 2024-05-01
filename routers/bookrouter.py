from fastapi import APIRouter, HTTPException, Depends
from db.database import Session
from db.models import Book
from schemas import book
import book_crud

br = APIRouter(
    prefix="/library"
)
async def get_db():
    async with Session as session:
        yield session

@br.get("/")
def root():
    return {"message":"Hello Library!"}

#Create
@br.post("/books", status_code=201, response_model=book.Book)
async def create_book(book: book.BookCreate):
    db = Session()
    data = await book_crud.create_book(db=db, book=book)
    db.close()
    return data
# Read
@br.get("/books")
async def get_books():
    db = Session()
    datas = await book_crud.get_books(db=db)
    db.close()
    return datas

@br.get("/books/search", status_code = 201,response_model = book.BookSearch)
async def search_book():
    db = Session()
    data = await book_crud.search_book(db=db, book = book)
    db.close()
    return data
# Update
@br.put("/books/{book_id}", response_model = book.BookUpdate)
async def update_book(id: int, book = book.Book):
    db = Session()
    data = await book_crud.update_book(db=db, book = book, book_id = id)
    db.close()
    print("Update Succeed")
    return data
# Delete
@br.delete("/books/{book_id}")
async def delete_book(id: int):
    db = Session()
    data = await book_crud.delete_book(db = db, book_id = id)
    db.close()
    print("Deletion Succeed")
    return data
