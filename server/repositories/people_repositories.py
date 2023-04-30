from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, insert, text, and_
from db.people import People
from db.users import Users
from typing import Optional


async def select_people(
    conn: AsyncSession, limit: int, page: int, user_id: Optional[int] = None
):
    query = select(People)
    if user_id:
        query = query.where(People.user_id == user_id)
    query = query.offset((page - 1) * limit).limit(limit)

    records = await conn.execute(query)

    return records.scalars().all()


async def get_total(conn: AsyncSession, user_id: Optional[int] = None) -> int:
    query = select(func.count(People.id))
    if user_id:
        query = query.where(People.user_id == user_id)

    total = await conn.execute(query)
    return total.scalar_one()


async def select_by_name(
    conn: AsyncSession, name: str, user_id: int | None
) -> People | None:
    query = select(People).where(
        and_(
            People.name == name,
            People.user_id == user_id if user_id else text("user_id IS NULL"),
        )
    )
    records = await conn.execute(query)
    result = records.scalar_one_or_none()
    return result


async def insert_person(
    conn: AsyncSession, name: str, user_id: int | None = None
) -> None:
    await conn.execute(
        insert(People).values(
            name=name, user_id=user_id, last_visit=datetime.now(), view_count=0
        )
    )
    await conn.commit()


async def update_person(conn: AsyncSession, name: str, view_count: int) -> None:
    await conn.execute(
        update(People)
        .where(People.name == name)
        .values(last_visit=datetime.now(), view_count=view_count + 1)
    )


async def select_users(conn: AsyncSession):
    query = (
        select(
            func.sum(People.view_count).label("view_count"), People.user_id, Users.name
        )
        .join(Users)
        .group_by(People.user_id, Users.name)
    )
    records = await conn.execute(query)
    return records.all()


async def select_people_with_views(conn: AsyncSession):
    result = await conn.execute(
        select(func.sum(People.view_count).label("count_sum"), People.name)
        .group_by(People.name)
        .order_by(func.sum(People.view_count).desc())
    )
    return result.all()
