from sqlalchemy.sql import insert, select
from db.init_db import Users


async def create_user(conn, name, email, password):
    await conn.execute(insert(Users).values(name=name, email=email, password=password))
    await conn.commit()


async def get_user_by_name(conn, name):
    result = await conn.execute(select(Users).where(Users.name == name))
    return result.scalar_one_or_none()
