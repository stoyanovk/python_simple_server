from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, insert, delete, and_
from db.prayers import Prayers
from db.users_prayers import Users_prayers
from db.users import Users


async def select_prayers(conn: AsyncSession, limit: int, page: int):
    query = (
        select(
            Prayers.id,
            Prayers.title,
            Prayers.user_id,
            func.substr(Prayers.text, 0, 100).label("description"),
        )
        .offset((page - 1) * limit)
        .limit(limit)
    )

    records = await conn.execute(query)

    return records.all()


async def get_total(conn: AsyncSession) -> int:
    query = select(func.count(Prayers.id))
    total = await conn.execute(query)
    return total.scalar_one()


async def select_prayer_by_id(conn: AsyncSession, prayer_id: int) -> Prayers | None:
    query = select(Prayers).where(Prayers.id == prayer_id)
    records = await conn.execute(query)
    result = records.scalar_one_or_none()
    return result


async def select_prayer_by_id_and_user_id(
    conn: AsyncSession, prayer_id: int, user_id: int
) -> Prayers | None:
    query = select(Prayers).where(
        and_(Prayers.id == prayer_id, Prayers.user_id == user_id)
    )
    records = await conn.execute(query)
    result = records.scalar_one_or_none()
    return result


async def insert_prayer(
    conn: AsyncSession,
    title: str,
    text: str,
    user_id: int,
) -> None:
    await conn.execute(insert(Prayers).values(title=title, text=text, user_id=user_id))
    await conn.commit()


async def update_prayer_data(
    conn: AsyncSession, prayer_id: int, title: str, text: str
) -> None:
    await conn.execute(
        update(Prayers).where(Prayers.id == prayer_id).values(title=title, text=text)
    )
    await conn.commit()


async def delete_prayer(conn: AsyncSession, prayer_id: int):
    await conn.execute(delete(Prayers).where(Prayers.id == prayer_id))
    await conn.commit()


async def get_assigned_prayers_by_user_id(conn: AsyncSession, user_id: int):
    query = (
        select(
            Prayers.id,
            Prayers.title,
            Users_prayers.user_id,
            func.substr(Prayers.text, 0, 100).label("description"),
        )
        .join(Users_prayers)
        .filter(Users_prayers.user_id == user_id)
    )

    records = await conn.execute(query)

    return records.all()


async def assign_prayer_to_user(
    conn: AsyncSession, user_ids: list[int], prayer_id: int
):
    insert_values = list(
        map(lambda user_id: {"user_id": user_id, "prayer_id": prayer_id}, user_ids)
    )
    await conn.execute(
        insert(Users_prayers),
        insert_values,
    )
    await conn.commit()


async def get_prayer_users(conn, prayer_id) -> tuple[int, str, int]:
    query = select(
        Users.id, Users.name, Users.role, Users.email, Users_prayers.prayer_id
    ).join(
        Users_prayers,
        and_(Users.id == Users_prayers.user_id, Users_prayers.prayer_id == prayer_id),
    )
    result = await conn.execute(query)
    return result.all()
