async def select_names(conn, limit, page):
    names_cursor = await conn.execute(
        f"SELECT * FROM names OFFSET {limit * (page - 1)} LIMIT {limit}"
    )
    records = await names_cursor.fetchall()
    names = [dict(q) for q in records]
    return names


async def get_total(conn):
    total_cursor = await conn.execute("SELECT COUNT(id) FROM names")
    total = await total_cursor.fetchone()
    return total[0]


async def select_by_name(conn, name):
    cursor = await conn.execute(f"SELECT name FROM names WHERE name = '{name}'")
    records = await cursor.fetchall()
    names = [dict(q) for q in records]
    return names


async def insert_name(conn, name):
    await conn.execute("INSERT INTO names (name) VALUES (%s)", (name))
