from sqlalchemy import MetaData, create_engine
from db.db import names
from config.config import CONFIG

DB = CONFIG.get("POSTGRES_DB")
USER = CONFIG.get("POSTGRES_USER")
PASSWORD = CONFIG.get("POSTGRES_PASSWORD")
HOST = CONFIG.get("POSTGRES_HOST")
PORT = CONFIG.get("POSTGRES_PORT")


db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[names])


if __name__ == "__main__":
    engine = create_engine(db_url)

    create_tables(engine)
