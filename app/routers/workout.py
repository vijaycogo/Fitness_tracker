from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import workout


# Creating APIRouter instance with 'workouts' tag and prefix '/workout'
router = APIRouter(
    prefix="/workout",
    tags=['workouts']
)

# Retrieving a database session
get_db = database.get_db

# Route for creating a new workout
@router.post('/',response_model=schemas.ShowWorkout, status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value == "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    created_workout =  workout.create(request, db, current_user.id)
    created_workout.exercise.exercise_type = created_workout.exercise.exercise_type.value
    created_workout.exercise.measurement_type = created_workout.exercise.measurement_type.value
    created_workout.exercise.major_minor_type = created_workout.exercise.major_minor_type.value
    return created_workout


# Route for getting all workouts
@router.get('/', response_model=List[schemas.ShowAllWorkout])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    workout_items =  workout.get_all(db)
    return workout_items

# Route for getting a specific workout by its ID
@router.get('/{id}', status_code=200, response_model=schemas.ShowWorkout)
def show(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # if current_user.role.value == "admin":
    #     raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    workout_item  = workout.show(id,db)

    workout_item.exercise.exercise_type = workout_item.exercise.exercise_type.value
    workout_item.exercise.measurement_type = workout_item.exercise.measurement_type.value
    workout_item.exercise.major_minor_type = workout_item.exercise.major_minor_type.value
    return workout_item

# Route for updating a workout.
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Workout, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value == "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    workout.update(id,request, db, current_user.id)
    return "User updated successfully"

# Route for deleting a workout
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return workout.destroy(id,db)
