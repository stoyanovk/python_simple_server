from sqlalchemy.sql import insert, select
from db.init_db import Users


async def create_user(conn, name, email, password):
    await conn.execute(insert(Users).values(name=name, email=email, password=password))


async def get_user_by_name(conn, name):
    cursor = await conn.execute(select([Users]).where(Users.name == name))
    return await cursor.fetchone()
