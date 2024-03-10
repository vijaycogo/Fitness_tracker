from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import exercise

router = APIRouter(
    prefix="/exercise",
    tags=['exercises']
)

get_db = database.get_db


@router.post('/',response_model=schemas.ShowExercise, status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Exercise, db: Session = Depends(get_db)):
    return exercise.create(request, db)

@router.get('/', response_model=List[schemas.ShowExercise])
def all(db: Session = Depends(get_db)):
    return exercise.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowExercise)
def show(id:int, db: Session = Depends(get_db)):
    return exercise.show(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Exercise, db: Session = Depends(get_db)):
    exercise.update(id,request, db)
    return "User updated successfully"


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return exercise.destroy(id,db)




# @router.post('/',response_model=schemas.ShowExercise, status_code=status.HTTP_201_CREATED,)
# def create(request: schemas.Exercise, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return exercise.create(request, db)

# @router.get('/', response_model=List[schemas.ShowExercise])
# def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return exercise.get_all(db)

# @router.get('/{id}', status_code=200, response_model=schemas.ShowExercise)
# def show(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return exercise.show(id,db)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id:int, request: schemas.Exercise, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     exercise.update(id,request, db)
#     return "User updated successfully"


# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return exercise.destroy(id,db)

