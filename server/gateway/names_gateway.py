from datetime import datetime


async def select_names(conn, limit, page):
    names_cursor = await conn.execute(
        f"SELECT * FROM names OFFSET {limit * (page - 1)} LIMIT {limit}"
    )
    records = await names_cursor.fetchall()
    return records


async def get_total(conn):
    total_cursor = await conn.execute("SELECT COUNT(id) FROM names")
    total = await total_cursor.fetchone()
    return total[0]


async def select_by_name(conn, name):
    cursor = await conn.execute("SELECT name FROM names WHERE name = %s", name)
    records = await cursor.fetchone()
    return records


async def insert_name(conn, name):
    await conn.execute(
        "INSERT INTO names (name, last_visit) VALUES (%s, %s)", (name, datetime.now())
    )


async def update_last_visit(conn, name):
    await conn.execute(
        "UPDATE names SET last_visit = %s WHERE name = %s", (datetime.now(), name)
    )
