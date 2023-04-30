from sqlalchemy.sql import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from db.users import Users
from typing import Optional


async def create_user(
    conn: AsyncSession, name: str, email: str, password: bytes
) -> None:
    await conn.execute(insert(Users).values(name=name, email=email, password=password))
    await conn.commit()


async def get_user_by_name(conn: AsyncSession, name: str) -> Optional[Users]:
    result = await conn.execute(select(Users).where(Users.name == name))
    return result.scalar_one_or_none()
