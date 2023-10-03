import strawberry
from strawberry.types import Info
from repositories.prayers_repositories import (
    select_prayers,
    select_prayer_by_id,
    get_prayer_users,
    get_assigned_prayers_by_user_id,
)
from repositories.user_repositories import get_user_by_id
from typing import Optional

from graph.user_graph import User


@strawberry.type
class Prayer:
    id: int
    title: str
    description: str
    user_id: int | None

    @strawberry.field
    async def user(self, info: Info) -> User | None:
        request = info.context["request"]
        session = request.app["db"]
        if not self.user_id:
            return None
        async with session() as conn:
            user = await get_user_by_id(conn, self.user_id)
        if not user:
            return None
        return User(id=user.id, email=user.email, role=user.role, name=user.name)

    @strawberry.field
    async def assigned_users(self, info: Info) -> list[User]:
        request = info.context["request"]
        session = request.app["db"]
        async with session() as conn:
            prayer_users = await get_prayer_users(conn, self.id)
        if not len(prayer_users):
            return []
        return [
            User(id=user.id, email=user.email, role=user.role, name=user.name)
            for user in prayer_users
        ]


async def prayers(
    self,
    info: Info,
    limit: Optional[int] = strawberry.UNSET,
    page: Optional[int] = strawberry.UNSET,
) -> list[Prayer]:
    request = info.context["request"]
    session = request.app["db"]
    limit = limit if limit else 5
    page = page if page else 1
    async with session() as conn:
        prayers = await select_prayers(conn, limit, page)
    if not len(prayers):
        return []
    return [
        Prayer(
            id=prayer.id,
            title=prayer.title,
            user_id=prayer.user_id,
            description="",
        )
        for prayer in prayers
    ]


async def prayer(self, info: Info, id: int) -> Prayer | None:
    request = info.context["request"]
    session = request.app["db"]
    async with session() as conn:
        prayer = await select_prayer_by_id(conn, int(id))
    if not prayer:
        return None
    return Prayer(
        id=prayer.id,
        title=prayer.title,
        user_id=prayer.user_id,
        description=prayer.text,
    )


async def assigned_prayers(self, info: Info, user_id: int) -> list[Prayer]:
    session = info.context["request"].app["db"]
    async with session() as conn:
        prayers = await get_assigned_prayers_by_user_id(conn, int(user_id))
    if not len(prayers):
        return []
    return [
        Prayer(
            id=prayer.id,
            title=prayer.title,
            user_id=prayer.user_id,
            description=prayer.text,
        )
        for prayer in prayers
    ]
