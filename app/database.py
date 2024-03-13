from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define and create SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/fitness.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create tables in the database
Base.metadata.create_all(bind=engine)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", reload=True)



# Function to retrieve a database session
def get_db():
    db = SessionLocal()         # Creating a database session
    try:
        yield db            # Yielding the session to be used in the context
    finally:
        db.close()          # Closing the session after its usage