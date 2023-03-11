from datetime import datetime
from sqlalchemy import select, func, update, insert, text, and_
from db.init_db import People, Users


async def select_people(conn, limit, page, user_id=None):
    query = select(People)
    if user_id:
        query = query.where(People.user_id == user_id)
    query = query.offset((page - 1) * limit).limit(limit)

    records = await conn.execute(query)

    return records.scalars().all()


async def get_total(conn, user_id=None):
    query = select(func.count(People.id))
    if user_id:
        query = query.where(People.user_id == user_id)

    total = await conn.execute(query)
    return total.scalar_one()


async def select_by_name(conn, name, user_id):
    # query = select(People).filter(People.name == name and People.user_id.is_(None))
    # WHERE name = 'Jake' AND not user_id;
    user_condition = People.user_id == user_id if user_id else text("user_id IS NULL")
    query = select(People).where(and_(People.name == name, user_condition))
    records = await conn.execute(query)
    result = records.scalar_one_or_none()
    return result


async def insert_person(conn, name, user_id=None):
    await conn.execute(
        insert(People).values(
            name=name, user_id=user_id, last_visit=datetime.now(), view_count=0
        )
    )
    await conn.commit()


async def update_person(conn, name, view_count):
    await conn.execute(
        update(People)
        .where(People.name == name)
        .values(last_visit=datetime.now(), view_count=view_count + 1)
    )


async def select_users(conn):
    query = (
        select(
            func.sum(People.view_count).label("view_count"), People.user_id, Users.name
        )
        .join(Users)
        .group_by(People.user_id, Users.name)
    )
    records = await conn.execute(query)
    return records.all()


async def select_people_with_views(conn):
    result = await conn.execute(
        select(func.sum(People.view_count).label("count_sum"), People.name)
        .group_by(People.name)
        .order_by(func.sum(People.view_count).desc())
    )
    return result.all()
