from aiohttp import web
from collections.abc import Sequence
import aiohttp_jinja2
from db.people import People
from lib.get_pagination import get_pagination, Button
from repositories.people_repositories import (
    select_people,
    get_total,
    select_by_name,
    insert_person,
    update_person,
    select_users,
    select_people_with_views,
)
from typing import List, TypedDict


async def main_page(request) -> web.StreamResponse:
    return aiohttp_jinja2.render_template(
        "index.html", request, context={"user": request.app.get("user", None)}
    )


def render_answer_template(request, is_name_exist, name):
    return aiohttp_jinja2.render_template(
        "answer.html",
        request,
        context={
            "is_name_exist": is_name_exist,
            "name": name,
            "user": request.app.get("user", None),
        },
    )


class CreatePersonBody(TypedDict):
    name: str


async def create_person(request) -> web.StreamResponse:
    data: CreatePersonBody = await request.post()
    name: str = data.get("name", "")
    user: dict = request.app.get("user", None)
    user_id: int | None = user["id"] if user else None

    if len(name.rstrip()) < 2:
        raise web.HTTPBadRequest(reason="Name must be more then 2 letters")

    async with request.app["db"]() as conn:
        async with conn.begin():
            person: People | None = await select_by_name(
                conn=conn, name=name, user_id=user_id
            )
            if person:
                await update_person(conn, person.name, person.view_count)
                return render_answer_template(request, True, name)
            else:
                await insert_person(conn, name, user_id)
                return render_answer_template(request, False, name)


async def get_people(request) -> web.HTTPFound | web.StreamResponse:
    async with request.app["db"]() as conn:
        async with conn.begin():
            path: str = request.path

            if request.rel_url.query.get("page", None) == "1":
                return web.HTTPFound(location=path)

            page: int = int(request.rel_url.query.get("page", 1))
            limit: int = int(request.rel_url.query.get("limit", 2))

            people: Sequence[People] = await select_people(
                conn=conn, limit=limit, page=page
            )

            total: int = await get_total(conn)

            pagination: List[Button] = get_pagination(
                page=page, limit=limit, total=total
            )

            return aiohttp_jinja2.render_template(
                "people.html",
                request,
                context={
                    "people": people,
                    "pagination": pagination,
                    "path": path,
                    "user": request.app.get("user", None),
                },
            )


async def get_user_people(request) -> web.HTTPFound | web.StreamResponse:
    user: dict | None = request.app.get("user", None)
    if not user:
        return web.HTTPFound(location="/people")
    async with request.app["db"]() as conn:
        path: str = request.path

        if request.rel_url.query.get("page", None) == "1":
            return web.HTTPFound(location=path)

        page: int = int(request.rel_url.query.get("page", 1))
        limit: int = int(request.rel_url.query.get("limit", 5))

        people: Sequence[People] = await select_people(
            conn=conn, limit=limit, page=page, user_id=user["id"]
        )

        total: int = await get_total(conn, user["id"])

        pagination: list[Button] = get_pagination(page=page, limit=limit, total=total)

        return aiohttp_jinja2.render_template(
            "people.html",
            request,
            context={
                "people": people,
                "pagination": pagination,
                "path": path,
                "user": request.app.get("user", None),
            },
        )


async def get_leader_board(request) -> web.StreamResponse:
    async with request.app["db"]() as conn:
        users = await select_users(conn)
        people = await select_people_with_views(conn)
        return aiohttp_jinja2.render_template(
            "leader-board.html",
            request,
            context={
                "people": people,
                "users": users,
                "user": request.app.get("user", None),
            },
        )
