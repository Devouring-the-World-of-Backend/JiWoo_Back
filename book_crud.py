from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from db import models
from schemas import book

'''Book'''
# Get all books
def get_books(db: AsyncSession, skip: int=0, limit: int=100):
    with db as session:
        result = session.execute(select(models.Book).offset(skip).limit(limit))
        return result.scalars.all()
    
# Search   
def search_book(
        db: AsyncSession, 
        title: Optional[str]=None, 
        author: Optional[str]=None,
        year: Optional[int]=None
        ):
    
    with db as session:
        result=[]
        if title:
            res = session.execute(select(models.Book).filter(models.Book.title == title))
            result.append(res.scalars.all())
        if author:
            res = session.execute(select(models.Book).filter(models.Book.author == author))
            result.append(res.scalars.all())
        if year:
            res = session.execute(select(models.Book).filter(models.Book.year == year))
            result.append(res.scalars.all())

        return result
    
# Create a book
def create_book(db: AsyncSession, book: book.BookCreate):
    data=models.Book(
        id = book.id,
        title = book.title,
        author = book.author,
        description = book.description,
        year = book.year
    ) # ** : 애스터리스크. 딕셔너리를 사용해서 키워드 인수로 값 넣기
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# Update a book
def update_book(db: AsyncSession, book_id: int, book: book.BookUpdate):
    with db as session:
        result = session.execute(select(models.Book).filter(models.Book.id == book_id))
        data = result.scalars().first()
        if data: # 검색 결과 존재시 업데이트
            update = book.dict()
            for key, value in update.items():
                setattr(data, key, value)
            db.commit()
            db.refresh(data)
            return data
        
# Delete a book
def delete_book(db: AsyncSession, book_id: int):
    with db as session:
        result = session.execute(select(models.Book).filter(models.Book.id == book_id))
        data = result.scalars.first()
        if data:
            session.delete(data)
            session.commit()
        else:
            return "No such data"
        return f"{book_id} was Deleted Successfully."
