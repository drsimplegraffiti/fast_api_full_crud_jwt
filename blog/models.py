from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

class Blog(Base):
    __tablename__ = "blogs"
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    body = Column(String(500), nullable=False)


class User(Base):
    __tablename__ = "users"
    id  = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    