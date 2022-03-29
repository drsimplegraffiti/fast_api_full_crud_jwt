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