from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import CONFIG

DB = CONFIG.get("POSTGRES_DB")
USER = CONFIG.get("POSTGRES_USER")
PASSWORD = CONFIG.get("POSTGRES_PASSWORD")
HOST = CONFIG.get("POSTGRES_HOST")
PORT = CONFIG.get("POSTGRES_PORT")

engine = create_async_engine(
    f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
)


async_session = async_sessionmaker(engine)
