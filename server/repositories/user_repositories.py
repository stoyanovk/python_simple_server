from sqlalchemy.sql import insert, select, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
from db.users import Users
from db.users_prayers import Users_prayers
from typing import Optional


async def create_user(
    conn: AsyncSession, name: str, email: str, password: bytes
) -> None:
    await conn.execute(insert(Users).values(name=name, email=email, password=password))
    await conn.commit()


async def get_user_by_name(conn: AsyncSession, name: str) -> Optional[Users]:
    result = await conn.execute(select(Users).where(Users.name == name))
    return result.scalar_one_or_none()


async def get_users(conn: AsyncSession, prayer_id):
    query = (
        select(Users.id, Users.name, Users_prayers.prayer_id)
        .outerjoin(
            Users_prayers,
            and_(
                Users.id == Users_prayers.user_id, Users_prayers.prayer_id == prayer_id
            ),
        )
        .where(text("prayer_id IS NULL"))
    )
    result = await conn.execute(query)
    return result.all()
