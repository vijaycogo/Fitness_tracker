# app/utility.py
from sqlalchemy.orm import Session
from database import SessionLocal
from app.models import Base


# Function to retrieve a database session
def get_db():
    db = SessionLocal()      # Creating a database session
    try:
        yield db
    finally:
        db.close()
