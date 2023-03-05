from aiohttp import web
import aiohttp_jinja2
from lib.get_pagination import get_pagination
from repositories.people import (
    select_people,
    get_total,
    select_by_name,
    insert_person,
    update_last_visit,
)


async def main_page(request):
    return aiohttp_jinja2.render_template(
        "index.html", request, context={"user": request.app.get("user", None)}
    )


async def create_person(request):
    data = await request.post()
    name = data.get("name")
    if len(name.rstrip()) < 2:
        raise web.HTTPBadRequest(reason="Name must be more then 2 letters")

    async with request.app["db"].acquire() as conn:
        row_name = await select_by_name(conn=conn, name=name)
        if row_name:
            fetched_name = row_name.get("name", "")
            await update_last_visit(conn, fetched_name)
            return aiohttp_jinja2.render_template(
                "answer.html",
                request,
                context={
                    "is_name_exist": True,
                    "name": name,
                    "user": request.app.get("user", None),
                },
            )
        else:
            user = request.app.get("user", None)

            # I donn't now how i can write it in different way
            if user:
                await insert_person(conn, name, user["id"])
            else:
                await insert_person(conn, name)

            return aiohttp_jinja2.render_template(
                "answer.html",
                request,
                context={
                    "is_name_exist": False,
                    "name": name,
                    "user": request.app.get("user", None),
                },
            )


async def get_people(request):
    async with request.app["db"].acquire() as conn:
        path = request.path

        if request.rel_url.query.get("page", None) == "1":
            return web.HTTPFound(location=path)

        page = int(request.rel_url.query.get("page", 1))
        limit = int(request.rel_url.query.get("limit", 5))

        people = await select_people(conn=conn, limit=limit, page=page)

        total = await get_total(conn)

        pagination = get_pagination(page=page, limit=limit, total=total)

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


async def get_user_people(request):
    user = request.app.get("user", None)
    if not user:
        return web.HTTPFound(location="/people")
    async with request.app["db"].acquire() as conn:
        path = request.path

        if request.rel_url.query.get("page", None) == "1":
            return web.HTTPFound(location=path)

        page = int(request.rel_url.query.get("page", 1))
        limit = int(request.rel_url.query.get("limit", 5))

        people = await select_people(
            conn=conn, limit=limit, page=page, user_id=user["id"]
        )

        total = await get_total(conn, user["id"])

        pagination = get_pagination(page=page, limit=limit, total=total)

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
