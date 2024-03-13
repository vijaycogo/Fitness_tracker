from sqlalchemy import Column, Integer, String, ForeignKey,Boolean,Enum,DateTime
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .enum.user_enum import UserRole
from .enum.exercise_enum import MajorMinorExerciseType
from .enum.exercise_enum import IndoorOutdoorExerciseType
from .enum.exercise_enum import MeasurementType

    
# Defining the User model class 
class User(Base):
    __tablename__ = 'users'

    # Columns for the users table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole), nullable=False)       # Column for user's role, using UserRole enum
    admin_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())         # Column for creation timestamp
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())    # Column for last update timestamp
    
    # Relationship with exercises table
    exercises = relationship('Exercise', back_populates="user")
    # Relationship with workouts table
    workout = relationship('Workout', back_populates="user")

# Defining the Exercise model class
class Exercise(Base):
    __tablename__ = 'exercises'

    # Columns for the exercises table
    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, index=True)
    exercise_type = Column(Enum(IndoorOutdoorExerciseType), nullable=False)
    measurement_type = Column(Enum(MeasurementType), nullable=False)
    per_count_second_unit_calorie = Column(Integer)
    added_by = Column(String, index=True)
    major_minor_type = Column(Enum(MajorMinorExerciseType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship with users table
    user = relationship("User", back_populates="exercises")
    # Relationship with workouts table
    workout = relationship("Workout", back_populates="exercise")

# Defining the Workout model class
class Workout(Base):
    __tablename__ = 'workouts'

    # Columns for the workouts table
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_set_by_admin = Column(Boolean, index=True)
    set_count = Column(Integer)
    repetition_count = Column(Integer)
    workout_time = Column(Integer)
    calorie_burn = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship with users table
    user = relationship("User", back_populates="workout")
    # Relationship with exercises table
    exercise = relationship("Exercise", back_populates="workout")