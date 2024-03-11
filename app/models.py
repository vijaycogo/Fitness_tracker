from sqlalchemy import Column, Integer, String, ForeignKey,Boolean,Enum
from .database import Base
from sqlalchemy.orm import relationship
# from enum import Enum as UserEnum


# class UserRole(UserEnum):
#     ADMIN = "admin"
#     CUSTOMER = "customer"

    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    #   role = Column(Enum(UserRole), nullable=False)
    admin_id = Column(Integer)
    
    exercises = relationship('Exercise', back_populates="user")
    workout = relationship('Workout', back_populates="user")


class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, index=True)
    exercise_type = Column(String, index=True)
    measurement_type = Column(String, index=True)
    per_count_second_unit_calorie = Column(Integer)
    added_by = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="exercises")
    workout = relationship("Workout", back_populates="exercise")


class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_set_by_admin = Column(Boolean, index=True)
    set_count = Column(Integer)
    repetition_count = Column(Integer)
    workout_time = Column(Integer)
    calorie_burn = Column(Integer)

    user = relationship("User", back_populates="workout")
    exercise = relationship("Exercise", back_populates="workout")