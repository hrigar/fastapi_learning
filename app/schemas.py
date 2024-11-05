import string
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean

class Post(BaseModel):
    title : str
    content :str

class PostResponse(Post):
    id: int
    published: bool

    class Config:
        arbitrary_types_allowed = True


class UserRespone(BaseModel):
    email: EmailStr
    id: int
    username: str