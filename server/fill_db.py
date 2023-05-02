from db.init_db import reg, get_async_engine
from config.config import get_config
from lib.password_utils import generate_password
from sqlalchemy.sql import insert
from db.users import Users
import asyncio


async def fill_db():
    async with get_async_engine(get_config()).begin() as session:
        await session.run_sync(reg.metadata.create_all)
        await session.execute(
            insert(Users),
            [
                {
                    "name": "Verder",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                },
                {
                    "name": "Tony",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                },
                {
                    "name": "John",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                },
                {
                    "name": "Jack",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                },
            ],
        )


asyncio.run(fill_db())
