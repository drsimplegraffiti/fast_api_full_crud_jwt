
from pydantic import BaseModel
2
class Blog(BaseModel):
    title: str
    body: str