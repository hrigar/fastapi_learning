from .database import Base
from sqlalchemy import create_engine, Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "postt"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)