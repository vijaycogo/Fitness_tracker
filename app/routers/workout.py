from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import workout

router = APIRouter(
    prefix="/workout",
    tags=['workouts']
)

get_db = database.get_db


@router.post('/',response_model=schemas.ShowWorkout, status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    created_workout =  workout.create(request, db, current_user.id)
    created_workout.exercise.exercise_type = created_workout.exercise.exercise_type.value
    created_workout.exercise.measurement_type = created_workout.exercise.measurement_type.value
    created_workout.exercise.major_minor_type = created_workout.exercise.major_minor_type.value
    return created_workout

@router.get('/', response_model=List[schemas.ShowAllWorkout])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    workout_items =  workout.get_all(db)
    return workout_items


@router.get('/{id}', status_code=200, response_model=schemas.ShowWorkout)
def show(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    workout_item  = workout.show(id,db)

    workout_item.exercise.exercise_type = workout_item.exercise.exercise_type.value
    workout_item.exercise.measurement_type = workout_item.exercise.measurement_type.value
    workout_item.exercise.major_minor_type = workout_item.exercise.major_minor_type.value
    return workout_item


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    workout.update(id,request, db, current_user.id)
    return "User updated successfully"


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return workout.destroy(id,db)
