import strawberry
from strawberry.types import Info
from repositories.user_repositories import get_user_by_id, get_all_users
from typing import Optional


@strawberry.type
class User:
    id: int
    email: str
    name: str
    role: str

    # @strawberry.field
    # async def prayers(self, info: Info) -> list[Prayer]:
    #     request = info.context["request"]
    #     session = request.app["db"]
    #     async with session() as conn:
    #         prayers = await get_assigned_prayers_by_user_id(conn, self.id)


async def users(
    self,
    info: Info,
    limit: Optional[int] = strawberry.UNSET,
    page: Optional[int] = strawberry.UNSET,
) -> list[User]:
    request = info.context["request"]
    session = request.app["db"]
    limit = limit if limit else 5
    page = page if page else 1
    async with session() as conn:
        users = await get_all_users(conn, limit, page)

    if len(users):
        return list(
            map(
                lambda user: User(
                    id=user.id, email=user.email, role=user.role, name=user.name
                ),
                users,
            )
        )
    return []


async def user(self, info: Info, id: int) -> User | None:
    request = info.context["request"]
    session = request.app["db"]
    async with session() as conn:
        user = await get_user_by_id(conn, int(id))
    if not user:
        return None
    return User(id=user.id, email=user.email, role=user.role, name=user.name)
