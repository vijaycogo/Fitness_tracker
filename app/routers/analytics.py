
from .. import schemas, database, models, oauth2
from fastapi import FastAPI, Query, APIRouter, HTTPException, Depends ,status
from app import schemas
from app.models import User, Workout, Exercise
from app.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt


router = APIRouter(
    prefix="/analytics",
    tags=['Analytics']
)


@router.get("/user/",response_model=List[schemas.ShowUser])
async def list_users(
    user_id: int = Query(None, description="Filter users by user_id"),
    role: str = Query(None, description="Filter users by role"),
    email: str = Query(None, description="Filter users by email"),
    admin_id: int = Query(None, description="Filter users by admin_id"),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    db = SessionLocal()
    try:
        query = db.query(User)
        if user_id is not None:
            query = query.filter(User.id == user_id)
        if role is not None:
            query = query.filter(User.role == role)
        if email is not None:
            query = query.filter(User.email == email)
        if admin_id is not None:
            query = query.filter(User.admin_id == admin_id)

        users = query.all()
        
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()



@router.get("/exercises/", response_model=List[schemas.AnalyticsExercise])
async def list_exercises(
    exercise_id: int = Query(None, description="Filter exercises by exercise_id"),
    exercise_name: str = Query(None, description="Filter exercises by exercise_name"),
    exercise_type: str = Query(None, description="Filter exercises by exercise_type"),
    measurement_type: str = Query(None, description="Filter exercises by measurement_type"),
    major_minor_type: str = Query(None, description="Filter exercises by major_minor_type"),
    added_by: str = Query(None, description="Filter exercises by added_by"),
    user_id: int = Query(None, description="Filter exercises by user_id"),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")

    db = SessionLocal()
    try:
        query = db.query(Exercise)
        if exercise_id is not None:
            query = query.filter(Exercise.id == exercise_id)
        if exercise_name is not None:
            query = query.filter(Exercise.exercise_name == exercise_name)
        if exercise_type is not None:
            query = query.filter(Exercise.exercise_type == exercise_type)
        if measurement_type is not None:
            query = query.filter(Exercise.measurement_type == measurement_type)
        if major_minor_type is not None:
            query = query.filter(Exercise.major_minor_type == major_minor_type)
        if added_by is not None:
            query = query.filter(Exercise.added_by == added_by)
        if user_id is not None:
            query = query.filter(Exercise.user_id == user_id)

        exercises = query.all()


        
        return exercises
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()



@router.get("/workouts/",response_model=List[schemas.ShowProgressWorkout])
async def list_workouts(
    workout_id: int = Query(None, description="Filter workouts by workout_id"),
    exercise_id: int = Query(None, description="Filter workouts by exercise"),
    user_id: int = Query(None, description="Filter workouts by user_id"),
    is_set_by_admin: bool = Query(None, description="Filter workouts by user_id"),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")

    db = SessionLocal()
    try:
        query = db.query(Workout)
        if workout_id is not None:
            query = query.filter(Workout.id == workout_id)
        if exercise_id is not None:
            query = query.filter(Workout.exercise_id == exercise_id)
        if user_id is not None:
            query = query.filter(Workout.user_id == user_id)
        if is_set_by_admin is not None:
            query = query.filter(Workout.is_set_by_admin == is_set_by_admin)

        workouts = query.all()
        return workouts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/progress-chart/")
async def progress_chart(
    start_date: date = Query(None, description="Filter by start date"),
    end_date: date = Query(None, description="Filter by end date"),
    user_id: int = Query(None, description="Filter by user_id"),
    exercise_id: int = Query(None, description="Filter workouts by exercise"),
    # current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # if current_user.role.value != "admin":
    #     raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")

    db = SessionLocal()
    try:
        query = db.query(Workout.created_at, func.sum(Workout.calorie_burn).label("total_calories_burnt"))
        if start_date is not None:
            query = query.filter(Workout.created_at >= start_date)
        if end_date is not None:
            query = query.filter(Workout.created_at <= end_date)
        if user_id is not None:
            query = query.filter(Workout.user_id == user_id)
        if exercise_id is not None:
            query = query.filter(Workout.exercise_id == exercise_id)    

        result = query.group_by(Workout.created_at).all()
        
        # Convert result to DataFrame for easier plotting
        df = pd.DataFrame(result, columns=['created_at', 'total_calories_burnt'])
        
        # Plotting the progress chart
        plt.plot(df['created_at'], df['total_calories_burnt'])
        plt.xlabel('Date')
        plt.ylabel('Total Calories Burnt')
        plt.title('Progress Chart')
        plt.show()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/workout-summary/")
async def workout_summary(
    start_date: date = Query(None, description="Filter by start date"),
    end_date: date = Query(None, description="Filter by end date"),
    user_id: int = Query(None, description="Filter by user_id"),
    # current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # if current_user.role.value != "admin":
    #     raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")

    db = SessionLocal()
    try:
        query = db.query(Workout)
        if start_date is not None:
            query = query.filter(Workout.created_at >= start_date)
        if end_date is not None:
            query = query.filter(Workout.created_at <= end_date)
        if user_id is not None:
            query = query.filter(Workout.user_id == user_id)

        workouts = query.all()
      

        return workouts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()