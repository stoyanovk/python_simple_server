from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session
from lib import password_utils
from lib.validators import Validator

from repositories.user import create_user as insert_user, get_user_by_name


def register_page(request):
    if request.app.get("user", None):
        return web.HTTPFound(location="/")
    return aiohttp_jinja2.render_template("register.html", request, {})


def login_page(request):
    if request.app.get("user", None):
        return web.HTTPFound(location="/")
    return aiohttp_jinja2.render_template("login.html", request, {})


async def create_user(request):
    try:
        body = await request.post()
        Validator(body["name"]).add(lambda a: not len(a), "Name can' be empty").add(
            lambda value: len(value) > 20, "Name can' be bigger then 20"
        ).check()

        Validator(body["email"]).add(lambda a: not len(a), "Email can' be empty").add(
            lambda value: "@" not in value, "Email should have @ symbol"
        ).check()

        Validator(body["password"]).add(
            lambda a: not len(a), "password can'n be empty"
        ).add(lambda a: len(a) < 4, "password length can'n be less that 4 symbols").add(
            lambda value: value != body["password_repeated"], "Passwords must be equal"
        ).check()

        password = password_utils.generate_password(body["password"])

        async with request.app["db"]() as conn:
            await insert_user(conn, body["name"], body["email"], password)

            return aiohttp_jinja2.render_template(
                "success.html",
                request,
                context={"register_success": True, "name": body["name"]},
            )
    except ValueError as err:
        raise web.HTTPBadRequest(reason=err)


async def login(request):
    try:
        body = await request.post()
        Validator(body["name"]).add(lambda a: not len(a), "Name can' be empty").check()
        Validator(body["password"]).add(
            lambda a: not len(a), "Password can' be empty"
        ).check()

        async with request.app["db"]() as conn:
            user = await get_user_by_name(conn, body["name"])
            if not user:
                raise web.HTTPBadRequest(reason="User with such login not found")

            is_correct_password = password_utils.check_password(
                body["password"], user.password
            )

            if not is_correct_password:
                raise web.HTTPBadRequest(reason="Wrong password")

            session = await get_session(request)

            session["user"] = {"id": user.id, "name": user.name}

            return aiohttp_jinja2.render_template(
                "success.html",
                request,
                context={"register_success": False, "name": body["name"]},
            )
    except ValueError as err:
        raise web.HTTPBadRequest(reason=err)


async def logout(request):
    session = await get_session(request)
    session["user"] = None
    return web.HTTPSeeOther(location="/")
