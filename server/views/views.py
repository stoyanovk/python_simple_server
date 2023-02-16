from aiohttp import web
import aiohttp_jinja2
from lib.get_pagination import get_pagination
from gateway.names_gateway import (
    select_names,
    get_total,
    select_by_name,
    insert_name,
    update_last_visit,
)


async def index(request):
    return aiohttp_jinja2.render_template("index.html", request, context={})


async def create_name(request):
    data = await request.post()
    name = data.get("name")
    if len(name.rstrip()) < 2:
        raise web.HTTPError(text="Name must be more then 2 letters")

    async with request.app["db"].acquire() as conn:
        names = await select_by_name(conn=conn, name=name)
        if len(names):
            fetched_name = names[0].get('name', '')
            await update_last_visit(conn, fetched_name)
            return aiohttp_jinja2.render_template(
                "answer.html", request, context={"is_name_exist": True, "name": name}
            )
        else:
            await insert_name(conn, name)
            return aiohttp_jinja2.render_template(
                "answer.html", request, context={"is_name_exist": False, "name": name}
            )


async def get_names(request):
    async with request.app["db"].acquire() as conn:
        path = request.path
        if request.rel_url.query.get("page", None) == "1":
            return web.HTTPFound(location=path)

        page = int(request.rel_url.query.get("page", 1))
        limit = int(request.rel_url.query.get("limit", 5))

        total = await get_total(conn)

        names = await select_names(conn=conn, limit=limit, page=page)

        if len(names) == 0:
            return web.HTTPFound(location=path)

        pagination = get_pagination(page=page, limit=limit, total=total)

        return aiohttp_jinja2.render_template(
            "names.html",
            request,
            context={"names": names, "pagination": pagination, "path": path},
        )
