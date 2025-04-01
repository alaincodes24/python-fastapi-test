from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: str
    password: str