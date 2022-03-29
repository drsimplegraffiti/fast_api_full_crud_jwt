from multiprocessing import synchronize
from fastapi import FastAPI, Depends, HTTPException, status, Response
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()



models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return blog

# Get all blogs
@app.get("/blogs")
async def read_all(db: Session = Depends(get_db)):
    blogs =  db.query(models.Blog).all()
    return blogs

# Get a blog by id
@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def read_one(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


# Delete a blog by id
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return "done"



