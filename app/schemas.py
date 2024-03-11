
from typing import List, Optional
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str

class UserUpdate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    name:str
    email:str
    password:str
    role:str
    admin_id: Optional[int] = None

class ShowUser(BaseModel):
    id:int
    name:str
    email:str
    role:str
    admin_id: Optional[int] = None
    # activities : List[Activity] =[]
    class Config():
        orm_mode = True

class ExerciseBase(BaseModel):
    exercise_name: str
    exercise_type:str
    measurement_type:str
    per_count_second_unit_calorie:int
    added_by:str

class Exercise(ExerciseBase):
    class Config():
        orm_mode = True


class ShowExercise(BaseModel):
    id:int
    exercise_name: str
    exercise_type:str
    measurement_type:str
    per_count_second_unit_calorie:int
    added_by:str
    user: ShowUser

    class Config():
        orm_mode = True



class WorkoutBase(BaseModel):
    exercise_id: int
    # user_id:int
    is_set_by_admin:bool
    set_count: Optional[int] = None
    repetition_count:Optional[int] = None
    workout_time:Optional[int] = None

class Workout(WorkoutBase):
    class Config():
        orm_mode = True


class ShowWorkout(BaseModel):
    id:int
    exercise_id: int
    user_id:int
    is_set_by_admin:bool
    set_count: int
    repetition_count:int
    calorie_burn: Optional[int] = None
    workout_time:Optional[int] = None
    
    
    # user: ShowUser
    exercise: ShowExercise

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
