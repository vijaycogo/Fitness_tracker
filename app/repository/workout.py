from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status
from app.enum.exercise_enum import MeasurementType

def get_all(db: Session):
    workouts = db.query(models.Workout).all()
    return workouts

def create(request: schemas.Workout, db: Session, user_id: int):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == request.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    calorie_burn = 0
    per_count_calorie = exercise.per_count_second_unit_calorie

    if exercise.measurement_type == MeasurementType.count:
        
        # Calculate calorie_burn based on the formula
        calorie_burn = request.repetition_count * request.set_count * per_count_calorie
    else:
        calorie_burn = request.workout_time * per_count_calorie

    new_workout = models.Workout(
        is_set_by_admin=request.is_set_by_admin,
        set_count=request.set_count,
        repetition_count=request.repetition_count,
        exercise_id=request.exercise_id,
        calorie_burn=calorie_burn,
        workout_time=request.workout_time,

        user_id=user_id,  # Assuming this is a valid user_id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout
    

def show(id:int,db:Session):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Workout with the id {id} is not available")
    return workout


def update(id:int, request:schemas.Workout, db:Session, user_id: int):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()

    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Workout with id {id} not found")

    exercise = db.query(models.Exercise).filter(models.Exercise.id == request.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    calorie_burn = 0
    per_count_calorie = exercise.per_count_second_unit_calorie

    
    if exercise.measurement_type == "count":
        
        # Calculate calorie_burn based on the formula
        calorie_burn = request.repetition_count * request.set_count * per_count_calorie
    else:
        calorie_burn = request.workout_time * per_count_calorie

    workout.exercise_id = request.exercise_id
    workout.user_id = user_id
    workout.is_set_by_admin = request.is_set_by_admin
    workout.set_count = request.set_count
    workout.repetition_count = request.repetition_count
    workout.calorie_burn = calorie_burn
    workout.workout_time = request.workout_time
    db.commit()
    return workout


def destroy(id:int,db: Session):
    workout = db.query(models.Workout).filter(models.Workout.id == id)

    if not workout.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Workout with id {id} not found")

    workout.delete(synchronize_session=False)
    db.commit()
    return 'done'
