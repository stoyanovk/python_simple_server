from sqlalchemy import Integer, String, MetaData, Table, Column
from aiopg.sa import create_engine
from config.config import CONFIG

meta = MetaData()

names = Table(
    "names",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(200), nullable=False),
)

DB = CONFIG.get("POSTGRES_DB")
USER = CONFIG.get("POSTGRES_USER")
PASSWORD = CONFIG.get("POSTGRES_PASSWORD")
HOST = CONFIG.get("POSTGRES_HOST")
PORT = CONFIG.get("POSTGRES_PORT")


async def pg_context(app):
    engine = await create_engine(
        database=DB,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )
    app["db"] = engine

    yield

    app["db"].close()
    await app["db"].wait_closed()
