from datetime import datetime
from sqlalchemy import select, func
from db.init_db import People


async def select_people(conn, limit, page, user_id=None):
    def get_query():
        query = select(People)
        if user_id:
            query = query.where(People.user_id == user_id)

        return query.offset((page - 1) * limit).limit(limit)

    names_cursor = await conn.execute(get_query())
    records = await names_cursor.fetchall()
    return records


async def get_total(conn, user_id=None):
    def get_query():
        query = select(func.count(People.id))
        if user_id:
            query = query.where(People.user_id == user_id)
        return query

    total_cursor = await conn.execute(get_query())
    total = await total_cursor.fetchone()
    return total[0]


async def select_by_name(conn, name):
    cursor = await conn.execute("SELECT name FROM people WHERE name = %s", name)
    records = await cursor.fetchone()
    return records


async def insert_person(conn, name, user_id=None):
    await conn.execute(
        "INSERT INTO people (name, last_visit, user_id) VALUES (%s, %s, %s)",
        (name, datetime.now(), user_id),
    )


async def update_last_visit(conn, name):
    await conn.execute(
        "UPDATE people SET last_visit = %s WHERE name = %s", (datetime.now(), name)
    )
