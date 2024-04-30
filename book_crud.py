from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from db import models
from schemas import book, user

'''Book'''
# Get all books
async def get_books(db: AsyncSession, skip: int=0, limit: int=100):
    async with db as session:
        result = await session.execute(select(models.Book).offset(skip).limit(limit))
        return result.scalars.all()
# Search   
async def search_book(
        db: AsyncSession, 
        title: Optional[str]=None, 
        author: Optional[str]=None,
        year: Optional[int]=None):
    
    async with db as session:
        result=[]
        if title:
            res = await session.execute(select(models.Book).filter(models.Book.title == title))
            result.append(res.scalars.all())
        if author:
            res = await session.execute(select(models.Book).filter(models.Book.author == author))
            result.append(res.scalars.all())
        if year:
            res = await session.execute(select(models.Book).filter(models.Book.year == year))
            result.append(res.scalars.all())

        return result
    
# Create a book
async def create_book(db: AsyncSession, book: book.BookCreate):
    data=models.Book(**book.dict()) # ** : 애스터리스크. 딕셔너리를 사용해서 키워드 인수로 값 넣기
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# Update a book
async def update_book(db: AsyncSession, book_id: int, book: book.BookUpdate):
    async with db as session:
        result = await session.execute(select(models.Book).filter(models.Book.id == book_id))
        data = result.scalars().first()
        if data: # 검색 결과 존재시 업데이트
            update = book.dict()
            for key, value in update.items():
                setattr(data, key, value)
            await db.commit()
            await db.refresh(data)
            return data
        
# Delete a book
async def delete_book(db: AsyncSession, book_id: int):
    async with db as session:
        result = await session.execute(select(models.Book).filter(models.Book.id == book_id))
        data = result.scalars.first()
        if data:
            await session.delete(data)
            await session.commit()
        else:
            return "No such data"
        return f"{book_id} was Deleted Successfully."


''' <limit and offset>
items - list of items paginated items.
limit - number of items per page.
offset - number of skipped items.
total - total number of items.
'''
