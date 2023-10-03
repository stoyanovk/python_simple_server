from db.init_db import reg, get_async_engine
from config.config import get_config
from lib.password_utils import generate_password
from sqlalchemy.sql import insert, select
from db.users import Users, Roles
from db.prayers import Prayers
from db.people import People
import asyncio

engine = get_async_engine(get_config())


async def fill_db():
    async with engine.begin() as session:
        # await session.run_sync(reg.metadata.drop_all)
        await session.run_sync(reg.metadata.create_all)
        await session.execute(
            insert(Users),
            [
                {
                    "name": "Verder",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.preacher,
                },
                {
                    "name": "Tony",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
                {
                    "name": "John",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
                {
                    "name": "Jack",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
                {
                    "name": "Bill",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
                {
                    "name": "Bob",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
                {
                    "name": "Will",
                    "email": "v@mail.com",
                    "password": generate_password("1234"),
                    "role": Roles.visitor,
                },
            ],
        )

    async with engine.connect() as session:
        result = await session.execute(
            select(Users).where(Users.role == Roles.preacher)
        )
        preacher: Users = result.fetchone()

    async with engine.begin() as session:
        await session.execute(
            insert(Prayers),
            [
                {
                    "title": "TEst",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
                {
                    "title": "TEst 1",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
                {
                    "title": "TEst 2",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
                {
                    "title": "TEst 3",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
                {
                    "title": "TEst 4",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
                {
                    "title": "TEst 5",
                    "text": "lorem TEst TEst TEst TEstTEstTEst TEst",
                    "user_id": preacher.id,
                },
            ],
        )

    async with engine.begin() as session:
        await session.execute(
            insert(People),
            [
                {
                    "name": "John",
                    "last_visit": None,
                    "user_id": preacher.id,
                    "view_count": 0,
                },
                {
                    "name": "Jack",
                    "last_visit": None,
                    "user_id": preacher.id,
                    "view_count": 0,
                },
                {
                    "name": "Kenny",
                    "last_visit": None,
                    "user_id": None,
                    "view_count": 0,
                },
                {
                    "name": "Kenny",
                    "last_visit": None,
                    "user_id": preacher.id,
                    "view_count": 0,
                },
                {
                    "name": "Kenny 1",
                    "last_visit": None,
                    "user_id": None,
                    "view_count": 0,
                },
                {
                    "name": "Kenny 2",
                    "last_visit": None,
                    "user_id": None,
                    "view_count": 0,
                },
                {
                    "name": "Kenny 3",
                    "last_visit": None,
                    "user_id": None,
                    "view_count": 0,
                },
            ],
        )


asyncio.run(fill_db())
