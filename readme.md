![carbon(2)](https://user-images.githubusercontent.com/70065792/160604942-0414cfcf-9395-4b3f-b6b0-42060cb5f43e.png)


#### Why fast

- Automatic docs --> Swagger Ui and Redoc Ui
- Pydantic
- Based on Open Standard [JSON Schema && Open API]
- Vscode Editor support

##### Security and Authentication

- HTTP Basic
- OAuth2 and JWT

---

##### Create virtual Environment

> pipenv install fastapi
> pipenv install uvicorn[standard]

##### Run server

> uvicorn main:app --reload

##### Path params

```python
# Import packages
from fastapi import FastAPI

# Instantiate app
app = FastAPI()

# Route handler using a decorator
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/{id}")
def blog(id: int):
    return {"message": f"Hello {id}"}

```

---

##### Query parameters

```python
@app.get("/blogs")
def blog(limit, published:bool=True, sort: Optional[str] = None):
    if published:
        return {"data": f"blogs limit to {limit}"}
    else:
        return {"data":f"blogs limit to {limit}"}


```

> http://127.0.0.1:8000/blogs?limit=3

##### request.body

```python
# Import packages
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# Instantiate app
app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
async def create_blog(blog: Blog):
    return {"data":blog}
```

##### changing port

```python
# Import packages
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Instantiate app
app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post("/blog")
async def create_blog(blog: Blog):
    return {"data":blog}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5678, debug=True)
```

- To run
  > python main.py

##### Using requirements.txt

> create a requirement.txt file and write it to it
> `fastapi uvicorn`

To run

> pip install -r requirements.txt

##### Running server nested in a folder

> uvicorn blog.main:app --reload

---

##### Crud server

```python
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


# Get all blogs
@app.get("/blogs")
async def read_all(db: Session = Depends(get_db)):
    blogs =  db.query(models.Blog).all()
    return blogs

# Get a blog by id
@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def read_one(id: int,response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blog

```

---

##### HTTPException

```

```
