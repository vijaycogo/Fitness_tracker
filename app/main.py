from fastapi import FastAPI
from . import  models
from .database import engine

from  .routers import exercise, workout, user, authentication, analytics

# Creating an instance of FastAPI
app = FastAPI()

# Creating database tables based on the defined models
models.Base.metadata.create_all(engine)

# Including routers for different endpoints in the application
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(workout.router)
app.include_router(analytics.router)
