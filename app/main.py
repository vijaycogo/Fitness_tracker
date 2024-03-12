from fastapi import FastAPI
from . import  models
from .database import engine

from  .routers import exercise, workout, user, authentication, analytics
app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(workout.router)
app.include_router(analytics.router)
