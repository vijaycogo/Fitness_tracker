from fastapi import FastAPI
from . import  models
from .database import engine

from  .routers import exercise, workout, user, authentication
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(workout.router)






















# app/main.py
# from app.schema.user_create_request import UserCreate
# from app.schema.user_response import UserResponse



# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.models import Base

# from app.services import create_user as services_create_user  # Rename the function here
# from app.services import read_user as services_read_user



# from app.utility import get_db
# app = FastAPI()

# from pydantic import BaseModel


# class UserCreate(BaseModel):
#     username: str
#     password: str

# class UserResponse(BaseModel):
#     id: int
#     username: str

# class UserUpdate(BaseModel):
#     username: str
#     password: str

# CRUD operations for User
# @app.post("/users", response_model=UserResponse,tags=["user"])
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     return services_create_user(db, user)  # Use the alias here

# @app.get("/users", response_model=UserResponse,tags=["user"])
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     return services_read_user(db, user_id)
# ... (other endpoints)
