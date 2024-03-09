from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException,status

def get_all(db: Session):
    activitys = db.query(models.Activity).all()
    return activitys

def create(request: schemas.Activity,db: Session):
    new_activity = models.Activity(name=request.name, description=request.description,user_id=1)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

def destroy(id:int,db: Session):
    activity = db.query(models.Activity).filter(models.Activity.id == id)

    if not activity.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Activity with id {id} not found")

    activity.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int,request:schemas.Activity, db:Session):
    activity = db.query(models.Activity).filter(models.Activity.id == id)

    if not activity.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Activity with id {id} not found")

    activity.update(request)
    db.commit()
    return 'updated'

def show(id:int,db:Session):
    activity = db.query(models.Activity).filter(models.Activity.id == id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Activity with the id {id} is not available")
    return activity