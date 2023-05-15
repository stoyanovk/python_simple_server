from aiohttp import web
from typing import List

import aiohttp_jinja2
from repositories.prayers_repositories import (
    insert_prayer,
    select_prayers,
    get_total,
    delete_prayer as remove_prayer,
    select_prayer_by_id,
    update_prayer_data,
    select_prayer_by_id_and_user_id,
    assign_prayer_to_user,
    get_assigned_prayers_by_user_id,
    get_prayer_users,
)
from repositories.user_repositories import get_users
from lib.get_pagination import get_pagination, Button


async def render_create_prayers(request):
    return aiohttp_jinja2.render_template(
        "create-prayer.html", request, {"user": request.app.get("user", None)}
    )


async def render_edit_prayers(request):
    async with request.app["db"]() as conn:
        prayer = await select_prayer_by_id(conn, int(request.match_info["id"]))
        if not prayer:
            return web.HTTPFound(location="/prayers")
        return aiohttp_jinja2.render_template(
            "create-prayer.html",
            request,
            {"is_edit": True, "prayer": prayer, "user": request.app.get("user", None)},
        )


async def create_prayer(request):
    user: dict = request.app.get("user", None)
    data: dict = await request.post()
    title: str | None = data.get("title", None)
    text: str | None = data.get("text", None)
    if not title:
        raise web.HTTPBadRequest(reason="Title can't be empty")
    if not text:
        raise web.HTTPBadRequest(reason="Text can't be empty")
    async with request.app["db"]() as conn:
        await insert_prayer(conn, title, text, user["id"])

        return web.HTTPFound(location="/prayers")


async def update_prayer(request):
    user: dict = request.app.get("user", None)
    data: dict = await request.post()
    title: str | None = data.get("title", None)
    text: str | None = data.get("text", None)
    prayer_id: int = int(request.match_info["id"])
    if not user or not user.get("id", None):
        raise web.HTTPBadRequest(reason="You should be auth")

    async with request.app["db"]() as conn:
        prayer = await select_prayer_by_id_and_user_id(conn, prayer_id, user["id"])

    if not prayer:
        raise web.HTTPBadRequest(reason="You shouldn't edit this prayer")
    if not title:
        raise web.HTTPBadRequest(reason="Title can't be empty")
    if not text:
        raise web.HTTPBadRequest(reason="Text can't be empty")
    async with request.app["db"]() as conn:
        await update_prayer_data(conn, prayer_id, title, text)
        return web.HTTPFound(location="/prayers")


async def get_prayers(request):
    path: str = request.path
    if request.rel_url.query.get("page", None) == "1":
        return web.HTTPFound(location=path)
    page: int = int(request.rel_url.query.get("page", 1))
    limit: int = int(request.rel_url.query.get("limit", 5))

    async with request.app["db"]() as conn:
        async with conn.begin():
            prayers = await select_prayers(conn=conn, limit=limit, page=page)

            total: int = await get_total(conn)

    pagination: List[Button] = get_pagination(page=page, limit=limit, total=total)
    return aiohttp_jinja2.render_template(
        "prayers.html",
        request,
        context={
            "prayers": prayers,
            "pagination": pagination,
            "path": path,
            "user": request.app.get("user", None),
        },
    )


async def get_prayers_by_id(request):
    async with request.app["db"]() as conn:
        prayer = await select_prayer_by_id(conn, int(request.match_info["id"]))
    if not prayer:
        return web.HTTPFound(location="/prayers")
    async with request.app["db"]() as conn:
        users_without_prayer = await get_users(conn, prayer.id)
        prayer_users = await get_prayer_users(conn, prayer.id)
    user = request.app.get("user", None)
    user_id = user["id"] if user else None
    return aiohttp_jinja2.render_template(
        "prayer.html",
        request,
        {
            "prayer": prayer,
            "can_edit": prayer.user_id == user_id,
            "user": request.app.get("user", None),
            "users": users_without_prayer,
            "prayer_users": prayer_users,
        },
    )


async def delete_prayer(request):
    prayer_id = request.match_info["id"]
    try:
        async with request.app["db"]() as conn:
            await remove_prayer(conn, int(prayer_id))
        return web.json_response(
            {"data": "ok"},
        )
    except TypeError:
        return web.json_response(
            {"error": "something went wrong"},
            status=400,
            content_type="application/json",
        )


async def assign_prayer(request):
    data = await request.post()
    prayer_id = request.match_info["id"]
    user_ids = list(data.values())
    # user = request.app.get("user", None)
    async with request.app["db"]() as conn:
        await assign_prayer_to_user(conn, user_ids, prayer_id)
    return web.HTTPFound(location="/prayers/assigned")


async def get_assigned_prayers(request):
    user = request.app.get("user", None)
    if not user:
        return web.HTTPFound(location="/login")
    async with request.app["db"]() as conn:
        prayers = await get_assigned_prayers_by_user_id(conn, user["id"])
    return aiohttp_jinja2.render_template(
        "prayers.html",
        request,
        {"prayers": prayers, "user": user},
    )
