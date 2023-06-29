from pydantic import BaseModel
from typing import List


class Articles(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Articles] = []

    class Config():
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class User(BaseModel):
    id: int
    username: str

    class Config():
        orm_mode = True


class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config():
        orm_mode = True


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
