from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int

    @validator("published_year")
    def future_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError(f"Published year cannot be in the future (current year: {current_year})")
        return value

class ResponseDeleteBook(BaseModel):
    message:str # response_message와 message는 사람이 보기 쉽게 하기 위해 구분함. 
    
# Custom Exception(GPT 도움)
class DatabaseConnectionError(Exception):
    def __init__(self):
        self.message = "Database connection error"

class UnauthorizedAccessError(Exception):
    def __init__(self):
        self.message = "Unauthorized access error"

app=FastAPI()
books_db=[
      Book(id=1, title="1984", author="George Orwell", description="19841984bigbrother",published_year=1949),
      Book(id=2, title="0909", author="George Orwell", description="animal", published_year=1909),
      Book(id=3, title="To Kill a Mockingbird", author="Harper Lee", description="mocking bird",published_year=1960),
      Book(id=4, title="To", author="Jisoo", description="mfdsaughp",published_year=2000)
]


@app.get("/",summary="루트 경로")
def root():
    return {"message":"Hello Library!"}

#Create
@app.post("/books", status_code=201, response_model=Book)
async def create_book(book:Book):
    books_db.append(book)
    return book
#Search
def research_func(
        title : Optional[str]=None, 
        author : Optional[str]=None,
        published_year : Optional[int]=None
                  ):
    res = books_db # 결과리스트 : 데이터베이스 내 모든 데이터로 시작
    if(title):
        print(title)
        tmpRes=[] # 일시적인 결과 보관 리스트 생성
        for idx, book in enumerate(books_db):
            if(title.lower() in book.title.lower()):
                tmpRes.append(book) # 제목 포함시 결과 보관
                print(tmpRes)

        if len(tmpRes)==0: # 검색 결과 없을 때
            return {"message":"No research result"}
        else:
            res=tmpRes
            return res # 결과 반환
    
    if(author):
        tmpRes=[]
        for idx, book in enumerate(books_db):
            if(author.lower() in book.author.lower()):
                tmpRes.append(book)

        if len(tmpRes)==0:
            return {"message":"No research result"}
        else:
            res=tmpRes
            return res
    
    if(published_year):
        tmpRes=[]
        for idx, book in enumerate(books_db):
            if(published_year==book.published_year):
                tmpRes.append(book)
         
        if len(tmpRes)==0:
            return {"message":"No research result"}
        else:
            res=tmpRes
            return res
        
@app.get("/books/search")
def searchBooks(
    title: Optional[str]=None,
    author: Optional[str]=None,
    published_year: Optional[int]=None
):
    return research_func(title, author, published_year)

#Read all
@app.get("/books", status_code=200, response_model=List[Book])
async def get_books():
    return books_db
#Read
@app.get("/books/{book_id}", status_code=200, response_model=Book)
async def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
#Update
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    for idx, existing_book in enumerate(books_db):
        if existing_book.id == book.id:
            books_db[idx]=book
            return book
    raise HTTPException(status_code=404, detail="Book has wrong information")
#Delete
@app.delete("/books/{book_id}", response_model=ResponseDeleteBook)
async def delete_book(book_id : int):
    for idx, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[idx]
            return {"message": f"{book_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

