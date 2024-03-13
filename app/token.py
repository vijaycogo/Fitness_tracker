from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas

# Secret key for token generation.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Algorithm for token generation
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30        # Expiration time for access token in minutes
from sqlalchemy.orm import Session
from app.models import User

# Function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify token
def verify_token(token: str, credentials_exception, db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email, db)
    if user is None:
        raise credentials_exception
    return user


# Function to get user from database based on email
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()