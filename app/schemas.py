from pydantic import BaseModel
from sqlalchemy import Boolean

class Post(BaseModel):
    title : str
    content :str

class PostResponse(Post):
    id: int
    published: bool

    class Config:
        arbitrary_types_allowed = True