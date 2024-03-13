
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status
from ..hashing import Hash
import re

# def create(request: schemas.User,db:Session):
#     new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),role=request.role, admin_id = request.admin_id)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


def is_valid_email(email):
    # Define a regular expression for basic email validation
    email_regex = r'^\S+@\S+\.\S+$'
    return re.match(email_regex, email) is not None

def create(request: schemas.User, db: Session):
    try:
        # Check if the provided email is valid
        if not is_valid_email(request.email):
            raise ValueError("Invalid email format")

        new_user = models.User(
            name=request.name,
            email=request.email,
            password=Hash.bcrypt(request.password),
            role=request.role,
            admin_id=request.admin_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def show(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

def get_all_user(db: Session):
    users = db.query(models.User).all()
    return users


def update(id: int, request: schemas.User, db: Session):
    # Query the user by ID
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    # Update user attributes
    db_user.name = request.name
    db_user.email = request.email
    db_user.password = Hash.bcrypt(request.password)
    db_user.role = request.role
    db_user.admin_id = request.admin_id

    # Commit the changes
    db.commit()
    
    # Return updated user attributes
    return db_user



def destroy(id: int, db: Session):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    db.delete(db_user)
    db.commit()