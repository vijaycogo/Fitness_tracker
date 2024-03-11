from typing import List
from fastapi import APIRouter
from .. import schemas, database, models, oauth2
# from app import database

from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    created_user = user.create(request, db)
    created_user.role = created_user.role.value
    return created_user


@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user_item =  user.show(id,db)
    user_item.role = user_item.role.value
    
    return user_item

@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    users = user.get_all_user(db)
    
    for individual_user in users:
        individual_user.role = individual_user.role.value
    return users


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user.update(id, request, db)
    return "User updated successfully"

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user.destroy(id, db)
    return "User deleted successfully"