from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import CONFIG

DB: str | None = CONFIG.get("POSTGRES_DB")
USER: str | None = CONFIG.get("POSTGRES_USER")
PASSWORD: str | None = CONFIG.get("POSTGRES_PASSWORD")
HOST: str | None = CONFIG.get("POSTGRES_HOST")
PORT: int | str | None = CONFIG.get("POSTGRES_PORT", 3000)

engine = create_async_engine(
    f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
)


async_session = async_sessionmaker(engine)
