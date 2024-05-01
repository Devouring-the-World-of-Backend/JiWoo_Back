# Create the pydantic models
from pydantic import BaseModel, Field
from typing import Optional


# Create a book data
class BookCreate(BaseModel):
    id: int
    title: str
    author: str
    description: str
    year: int

# Response Model
class Book(BaseModel):
    id: int
    borrower_id: int

    class Config:
        ord_mode=True
'''FastAPI에서 Pydantic으로 응답받기 위해서는 JSON 파서 구현이 필요함. orm_mode를 쓰면
JSON 파서를 구현하지 않아도 Pydantic 모델로 변환해주고 JSON 포맷으로 인코딩해준다.
응답 모델에 필요함. ORM Model 데이터 -> Pydantic 모델 변환 로직'''

# Update Model
class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    description : Optional[str] = None
    year: Optional[int] = None

class BookSearch(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
