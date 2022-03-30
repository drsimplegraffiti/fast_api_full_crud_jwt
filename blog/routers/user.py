from typing import List
from fastapi import APIRouter, status, FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash


router = APIRouter(
     prefix ="/user",
    tags=["Users"]
)
get_db= database.get_db
# create user account

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user



# Get user information
@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return user

