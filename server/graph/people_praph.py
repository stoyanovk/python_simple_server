import strawberry
from strawberry.types import Info
from repositories.user_repositories import get_user_by_id
from repositories.people_repositories import select_by_id, select_people
from graph.user_graph import User
from typing import Optional


@strawberry.type
class People:
    id: int
    name: str
    last_visit: str | None
    view_count: int
    user_id: int | None

    @strawberry.field
    async def user(self, info: Info) -> None | User:
        session = info.context["request"].app["db"]
        if not self.user_id:
            return None
        async with session() as conn:
            user = await get_user_by_id(conn, self.user_id)
        if not user:
            return None
        return User(id=user.id, email=user.email, role=user.role, name=user.name)


async def people(
    self,
    info: Info,
    limit: Optional[int] = strawberry.UNSET,
    page: Optional[int] = strawberry.UNSET,
    user_id: Optional[int] = strawberry.UNSET,
) -> list[People]:
    request = info.context["request"]
    session = request.app["db"]
    limit = limit if limit else 5
    page = page if page else 1
    async with session() as conn:
        result_people = await select_people(conn, limit, page, user_id)
    if len(result_people):
        return [
            People(
                id=person.id,
                name=person.name,
                last_visit=str(person.last_visit),
                view_count=person.view_count,
                user_id=person.user_id,
            )
            for person in result_people
        ]

    return []


async def person(self, info: Info, id: int) -> People | None:
    request = info.context["request"]
    session = request.app["db"]
    async with session() as conn:
        person = await select_by_id(conn, int(id))
    if not person:
        return None
    return People(
        id=person.id,
        name=person.name,
        last_visit=str(person.last_visit),
        view_count=person.view_count,
        user_id=person.user_id,
    )
