from typing import List
from fastapi import APIRouter, status, FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..repository import user

router = APIRouter(
     prefix ="/user",
    tags=["Users"]
)
get_db= database.get_db
# create user account

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def create_user(request: schemas.User, db:Session = Depends(get_db)):
    return user.create(request,db)


# Get user information
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def get_user(id: int, db:Session = Depends(get_db)):
    return user.show(id,db)

