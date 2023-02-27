from sqlalchemy import Column, Integer, String
from db.init_db import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
