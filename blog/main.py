from typing import List
from multiprocessing import synchronize
from fastapi import FastAPI, Depends, HTTPException, status, Response
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()



models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root():
    return {"message": "Home page"}

# Create a blog
@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Update a blog by id
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return "updated"

# Get all blogs
@app.get("/blogs", status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
async def read_all(db: Session = Depends(get_db)):
    blogs =  db.query(models.Blog).all()
    return blogs

# Get a blog by id
@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def read_one(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


# Delete a blog by id
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"



# create user account

@app.post("/user", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user



# Get user information
@app.get("/user/{id}", status_code=status.HTTP_201_CREATED, response_model = schemas.ShowUser)
async def get_user(id: int, db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# person = [{
#     "name": "John",
#     "age": 30,
#     "occupation": "developer"
# },
# {
#     "name": "jane",
#     "age": 30,
#     "occupation": "developer"
# }]

# @app.get("/users/")
# async def read_all_users():
#     return person