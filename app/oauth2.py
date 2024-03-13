from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token

from fastapi import APIRouter,Depends,status
from app import database
get_db = database.get_db
from sqlalchemy.orm import Session

# Initializing OAuth2PasswordBearer instance for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to get the current user based on the provided token
def get_current_user(data: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    # Creating an HTTPException for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verifying the provided token and getting the user
    user= token.verify_token(data, credentials_exception,db)
    return user
