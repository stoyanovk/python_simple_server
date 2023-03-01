from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import declarative_base
from config.config import CONFIG

DB = CONFIG.get("POSTGRES_DB")
USER = CONFIG.get("POSTGRES_USER")
PASSWORD = CONFIG.get("POSTGRES_PASSWORD")
HOST = CONFIG.get("POSTGRES_HOST")
PORT = CONFIG.get("POSTGRES_PORT")

Base = declarative_base()


class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    last_visit = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(LargeBinary(), nullable=False)


db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(db_url)


def init_db():
    Base.metadata.create_all(engine)
