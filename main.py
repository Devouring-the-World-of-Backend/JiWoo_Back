from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from db.models import Base
from db.database import Session, engine
from routers.bookrouter import br
from routers.userrouter import ur

Base.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():
    db = Session()
    try:
        yield db # connection to database
    finally:
        db.close()


# Custom Exception(GPT 도움)
class DatabaseConnectionError(Exception):
    def __init__(self):
        self.message = "Database connection error"

class UnauthorizedAccessError(Exception):
    def __init__(self):
        self.message = "Unauthorized access error"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 도메인 전부 허용
    allow_credentials=True,
    allow_methods=["*"], # 허용할 HTTP 메소드
    allow_headers=["*"] # 허용할 HTTP 헤더
)
 
# Router Registration
app.include_router(br)
app.include_router(ur)