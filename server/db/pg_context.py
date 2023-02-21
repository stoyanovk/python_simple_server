from aiopg.sa import create_engine


async def pg_context(app):
    engine = await create_engine(
        database=app["config"].get("POSTGRES_DB"),
        user=app["config"].get("POSTGRES_USER"),
        password=app["config"].get("POSTGRES_PASSWORD"),
        host=app["config"].get("POSTGRES_HOST"),
        port=app["config"].get("POSTGRES_PORT"),
    )
    app["db"] = engine

    yield

    app["db"].close()
    await app["db"].wait_closed()
