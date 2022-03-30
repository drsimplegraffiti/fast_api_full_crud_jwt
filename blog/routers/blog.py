from typing import List
from fastapi import APIRouter, status, FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from ..repository import blog

router = APIRouter(
    prefix ="/blog",
    tags=["Blogs"]
)
get_db =database.get_db

@router.get('/home',  tags=["root"])
async def root():
    return {"message": "Home page"}


# Get all blogs
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
async def read_all(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user) ):
    return blog.get_all(db)
    


# Create a blog
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)



# Update a blog by id
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id:int, request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)


# Get a blog by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def read_one(id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id,db)


# Delete a blog by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)