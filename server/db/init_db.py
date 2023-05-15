from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import registry


reg = registry()


def get_async_engine(config):
    USER = config["POSTGRES_USER"]
    PASSWORD = config["POSTGRES_PASSWORD"]
    HOST = config["POSTGRES_HOST"]
    PORT = config["POSTGRES_PORT"]
    DB = config["POSTGRES_DB"]
    return create_async_engine(
        f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    )


def get_async_session(config):
    return async_sessionmaker(get_async_engine(config))


async def init_db(config):
    async with get_async_engine(config).begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(reg.metadata.create_all)
