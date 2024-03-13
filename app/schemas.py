
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .enum.user_enum import UserRole
from .enum.exercise_enum import MeasurementType
from .enum.exercise_enum import MajorMinorExerciseType
from .enum.exercise_enum import IndoorOutdoorExerciseType


# Response model for User
class UserResponse(BaseModel):
    id: int
    username: str


# Model for updating User
class UserUpdate(BaseModel):
    username: str
    password: str

# Base model for User
class User(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole
    admin_id: Optional[int] = None      # Admin ID of the user (optional)

    class Config:
        orm_mode = True         # ORM mode for Pydantic model

# Detailed model for displaying User
class ShowUser(BaseModel):
    id:int
    name:str
    email:str
    role:UserRole
    admin_id: Optional[int] = None
    created_at:datetime
    updated_at:datetime
    # activities : List[Activity] =[]
    class Config():
        orm_mode = True

# Base model for Exercise
class ExerciseBase(BaseModel):
    exercise_name: str
    exercise_type:IndoorOutdoorExerciseType
    measurement_type:MeasurementType
    per_count_second_unit_calorie:int
    added_by:str
    major_minor_type:MajorMinorExerciseType

# Detailed model for Analytics on Exercise
class AnalyticsExercise(BaseModel):
    exercise_name: str
    exercise_type:IndoorOutdoorExerciseType
    measurement_type:MeasurementType
    per_count_second_unit_calorie:int
    added_by:str
    major_minor_type:MajorMinorExerciseType
    created_at:datetime

# Detailed model for Exercise
class Exercise(ExerciseBase):
    class Config():
        orm_mode = True

# Detailed model for displaying Exercise
class ShowExercise(BaseModel):
    id:int
    exercise_name: str
    exercise_type:str
    measurement_type:str
    per_count_second_unit_calorie:int
    added_by:str
    created_at:datetime
    updated_at:datetime
    user: ShowUser

    class Config():
        orm_mode = True


# Base model for Workout
class WorkoutBase(BaseModel):
    exercise_id: int
    # user_id:int
    is_set_by_admin:bool
    set_count: Optional[int] = None
    repetition_count:Optional[int] = None
    workout_time:Optional[int] = None

# Detailed model for Workout
class Workout(WorkoutBase):
    class Config():
        orm_mode = True

# Detailed model for displaying Workout
class ShowWorkout(BaseModel):
    id:int
    exercise_id: int
    user_id:int
    is_set_by_admin:bool
    set_count: int
    repetition_count:int
    calorie_burn: Optional[int] = None
    workout_time:Optional[int] = None
    created_at:datetime
    updated_at:datetime
    
    
    # user: ShowUser
    exercise: ShowExercise

    class Config():
        orm_mode = True

# Model for displaying all Workout without associated user and exercise details
class ShowAllWorkout(BaseModel):
    id:int
    exercise_id: int
    user_id:int
    is_set_by_admin:bool
    set_count: int
    repetition_count:int
    calorie_burn: Optional[int] = None
    workout_time:Optional[int] = None
    
    
    # user: ShowUser
    # exercise: ShowExercise

    class Config():
        orm_mode = True

# Base nodel to show Workout Progress
class ShowProgressWorkout(BaseModel):
    id:int
    exercise_id: int
    user_id:int
    is_set_by_admin:bool
    set_count: int
    repetition_count:int
    calorie_burn: Optional[int] = None
    workout_time:Optional[int] = None
    created_at: datetime
    
    class Config():
        orm_mode = True

# Model for user login
class Login(BaseModel):
    username: str
    password:str

# Model for token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Model for token data
class TokenData(BaseModel):
    email: Optional[str] = None
