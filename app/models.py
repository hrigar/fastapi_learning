from .database import Base
from sqlalchemy import  TIMESTAMP, Nullable, create_engine, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()') )


class User(Base):
    __tablename__="post"

    email = Column(String, nullable=False)
    password = Column(String, nullable=False)