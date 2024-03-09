from typing import List
from fastapi import APIRouter
from .. import database, schemas, models

# from app import database

from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

@router.get('/',response_model=List[schemas.ShowUser])
def get_all_user(db: Session = Depends(get_db)):
    return user.get_all_user(db)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db: Session = Depends(get_db)):
    return user.show(id,db)

