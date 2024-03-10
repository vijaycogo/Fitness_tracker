from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import workout

router = APIRouter(
    prefix="/workout",
    tags=['workouts']
)

get_db = database.get_db


@router.post('/',response_model=schemas.ShowWorkout, status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Workout, db: Session = Depends(get_db)):
    user_id =1
    # exersice_id = 1
    return workout.create(request, db,user_id)

@router.get('/', response_model=List[schemas.ShowWorkout])
def all(db: Session = Depends(get_db)):
    return workout.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowWorkout)
def show(id:int, db: Session = Depends(get_db)):
    return workout.show(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Workout, db: Session = Depends(get_db)):
    workout.update(id,request, db)
    return "User updated successfully"


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return workout.destroy(id,db)




# @router.post('/',response_model=schemas.ShowWorkout, status_code=status.HTTP_201_CREATED,)
# def create(request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return workout.create(request, db)

# @router.get('/', response_model=List[schemas.ShowWorkout])
# def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return workout.get_all(db)

# @router.get('/{id}', status_code=200, response_model=schemas.ShowWorkout)
# def show(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return workout.show(id,db)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id:int, request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     workout.update(id,request, db)
#     return "User updated successfully"


# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return workout.destroy(id,db)



