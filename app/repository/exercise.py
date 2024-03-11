from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status

def get_all(db: Session):
    exercises = db.query(models.Exercise).all()
    return exercises

def create(request: schemas.Exercise, db: Session, user_id: int):
    new_exercise = models.Exercise(exercise_name=request.exercise_name, exercise_type=request.exercise_type, measurement_type=request.measurement_type, per_count_second_unit_calorie=request.per_count_second_unit_calorie, added_by=request.added_by, major_minor_type= request.major_minor_type, user_id=user_id)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

def show(id:int,db:Session):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exercise with the id {id} is not available")
    return exercise


def update(id:int,request:schemas.Exercise, db:Session):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()

    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exercise with id {id} not found")

    exercise.exercise_name = request.exercise_name
    exercise.exercise_type = request.exercise_type
    exercise.measurement_type = request.measurement_type
    exercise.per_count_second_unit_calorie = request.per_count_second_unit_calorie
    exercise.added_by = request.added_by

    # Commit the changes
    db.commit()
    # Return updated user attributes
    return exercise


def destroy(id:int,db: Session):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id)

    if not exercise.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exercise with id {id} not found")

    exercise.delete(synchronize_session=False)
    db.commit()
    return 'done'
