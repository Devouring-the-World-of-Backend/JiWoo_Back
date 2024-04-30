from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from db import models
from schemas import user

'''User'''
# Get all Users
async def get_users(db: AsyncSession, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Find user using user_id
async def get_user(db: AsyncSession, user_id : int):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

# Find user using email
async def get_user_by_email(db: AsyncSession, email : str):
    return db.query(models.User).filter(models.User.email == email).first()


# Create User data
async def create_user(db: AsyncSession, user: user.UserCreate): 
    fake_hashed_password = user.password+'notreallyhashed'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update User data
async def update_user(db: AsyncSession, user: user.UserUpdate):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.name == user.name, models.User.email == user.email))
        db_user = result.scalars.first()
        update = user.dict()
        if db_user:
            for key, value in update.items():
                setattr(db_user, key, value)
            await db.commit()
            await db.refresh(db_user)
            return db_user




