# app/utility.py
from sqlalchemy.orm import Session
from db import SessionLocal
from app.models import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
