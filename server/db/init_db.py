from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config.config import CONFIG

DB = CONFIG.get("POSTGRES_DB")
USER = CONFIG.get("POSTGRES_USER")
PASSWORD = CONFIG.get("POSTGRES_PASSWORD")
HOST = CONFIG.get("POSTGRES_HOST")
PORT = CONFIG.get("POSTGRES_PORT")

Base = declarative_base()

db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

engine = create_engine(db_url)


def init_db():
    Base.metadata.create_all(engine)
