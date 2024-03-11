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
    created_exercise =  exercise.create(request, db)
    created_exercise.exercise_type = created_exercise.exercise_type.value
    created_exercise.measurement_type = created_exercise.measurement_type.value
    created_exercise.major_minor_type = created_exercise.major_minor_type.value
    return created_exercise


@router.get('/', response_model=List[schemas.ShowExercise])
def all(db: Session = Depends(get_db)):
    exercise_items = exercise.get_all(db)
    for exercise_item in exercise_items:
        exercise_item.exercise_type = exercise_item.exercise_type.value
        exercise_item.measurement_type = exercise_item.measurement_type.value
        exercise_item.major_minor_type = exercise_item.major_minor_type.value
    return exercise_items

@router.get('/{id}', status_code=200, response_model=schemas.ShowExercise)
def show(id:int, db: Session = Depends(get_db)):
    exercise_item =  exercise.show(id,db)
    exercise_item.exercise_type = exercise_item.exercise_type.value
    exercise_item.measurement_type = exercise_item.measurement_type.value
    exercise_item.major_minor_type = exercise_item.major_minor_type.value
    return exercise_item


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Exercise, db: Session = Depends(get_db)):
    exercise.update(id,request, db)
    return "Exercise updated successfully"


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    return exercise.destroy(id,db)

