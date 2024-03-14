from typing import List
from fastapi import APIRouter, HTTPException
from .. import schemas, database, models, oauth2
# from app import database

from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from ..repository import user
from ..hashing import Hash
import re
from sqlalchemy.exc import IntegrityError



# Initializing APIRouter instance with 'Users' tag and '/user' prefix
router = APIRouter(
    prefix="/user",
    tags=['Users']
)

# Function to retrieve a database session
get_db = database.get_db

def is_valid_email(email):
    # Define a regular expression for basic email validation
    email_regex = r'^\S+@\S+\.\S+$'
    return re.match(email_regex, email) is not None


@router.post('/', response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(get_db)):
    try:
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

    except IntegrityError as ie:
        # Handle database integrity errors
        db.rollback()  # Rollback the transaction
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )




# @router.post('/', response_model=schemas.ShowUser)
# def create(request: schemas.User, db: Session = Depends(get_db)):
#     try:
#         # Check if the provided email is valid
#         if not is_valid_email(request.email):
#             raise ValueError("Invalid email format")

#         new_user = models.User(
#             name=request.name,
#             email=request.email,
#             password=Hash.bcrypt(request.password),
#             role=request.role,
#             admin_id=request.admin_id
#         )

#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)

#         return new_user
#     except ValueError as ve:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=str(ve)
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=str(e)
#         )

@router.get('/{id}',response_model=schemas.ShowUser)
def get_user(id:int,db: Session = Depends(get_db)):
    user_item =  user.show(id,db)
    user_item.role = user_item.role.value
    
    return user_item

# Route for retrieving all users
@router.get('/', response_model=List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    users = user.get_all_user(db)
    
    for individual_user in users:
        individual_user.role = individual_user.role.value
    return users


# Route for updating a user by ID.
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role.value == "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource.")
    user.update(id, request, db)
    return "User updated successfully"


# Route for deleting a user by ID.
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user.destroy(id, db)
    return "User deleted successfully"