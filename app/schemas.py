
from typing import List, Optional
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    description:str

class Activity(ActivityBase):
    class Config():
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str

class UserUpdate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    id:int
    name:str
    email:str
    activities : List[Activity] =[]
    class Config():
        orm_mode = True



class ShowActivity(BaseModel):
    name: str
    description:str
    creator: ShowUser

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
