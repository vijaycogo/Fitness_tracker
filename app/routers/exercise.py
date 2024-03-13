from typing import List
from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from ..repository import exercise

# Initializing APIRouter instance with prefix and tags
router = APIRouter(
    prefix="/exercise",
    tags=['exercises']
)

# Function to retrieve a database session
get_db = database.get_db

# Route for creating a new exercise
@router.post('/',response_model=schemas.ShowExercise, status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Exercise, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Creating a new exercise in the database
    created_exercise =  exercise.create(request, db, current_user.id)
    created_exercise.exercise_type = created_exercise.exercise_type.value
    created_exercise.measurement_type = created_exercise.measurement_type.value
    created_exercise.major_minor_type = created_exercise.major_minor_type.value
    return created_exercise


# Route for retrieving all exercises
@router.get('/', response_model=List[schemas.ShowExercise])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Retrieving all exercises from the database
    exercise_items = exercise.get_all(db)
    for exercise_item in exercise_items:
        exercise_item.exercise_type = exercise_item.exercise_type.value
        exercise_item.measurement_type = exercise_item.measurement_type.value
        exercise_item.major_minor_type = exercise_item.major_minor_type.value
    return exercise_items


# Route for retrieving a specific exercise by ID
@router.get('/{id}', status_code=200, response_model=schemas.ShowExercise)
def show(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Retrieving the exercise from the database by ID
    exercise_item =  exercise.show(id,db)
    exercise_item.exercise_type = exercise_item.exercise_type.value
    exercise_item.measurement_type = exercise_item.measurement_type.value
    exercise_item.major_minor_type = exercise_item.major_minor_type.value
    return exercise_item


# Route for updating an existing exercise by ID
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Exercise, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Updating the exercise in the database by ID
    exercise.update(id,request, db)
    return "Exercise updated successfully"


# Route for deleting an existing exercise by ID
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return exercise.destroy(id,db)

