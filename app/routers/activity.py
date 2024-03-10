# from typing import List
# from fastapi import APIRouter,Depends,status,HTTPException
# from .. import schemas, database, models, oauth2
# from sqlalchemy.orm import Session
# from ..repository import activity

# router = APIRouter(
#     prefix="/activity",
#     tags=['activities']
# )

# get_db = database.get_db

# @router.get('/', response_model=List[schemas.ShowActivity])
# def all(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return activity.get_all(db)


# @router.post('/', status_code=status.HTTP_201_CREATED,)
# def create(request: schemas.Activity, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return activity.create(request, db)

# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return activity.destroy(id,db)


# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id:int, request: schemas.Activity, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return activity.update(id,request, db)


# @router.get('/{id}', status_code=200, response_model=schemas.ShowActivity)
# def show(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return activity.show(id,db)