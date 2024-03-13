from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status
from ..hashing import Hash


# Function to create a new user entry in the database
def create(request: schemas.User,db:Session):
    # Creating a new User object with the provided data
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password),role=request.role, admin_id = request.admin_id)
    db.add(new_user)    # Adding the new user to the database
    db.commit()  # Committing the transaction
    db.refresh(new_user)    # Refreshing the object to reflect changes
    return new_user


# Function to retrieve a single user by its ID
def show(id:int,db:Session):
    # Querying the user by its ID
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:    # If User not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user


# Function to retrieve all users from the database
def get_all_user(db: Session):
    users = db.query(models.User).all()
    return users

# Function to update an existing user entry
def update(id: int, request: schemas.User, db: Session):
    # Query the user by ID
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:     #If User not found
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


# Function to delete a user entry from the database
def destroy(id: int, db: Session):
    # Querying the user by its ID
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    db.delete(db_user)      # Deleting the user entry from the database
    db.commit()