from aiohttp import web
import jinja2
import aiohttp_jinja2

from routes.people import routes as people_routes
from routes.auth import routes as auth_routes

from db.pg_context import pg_context
from config.config import CONFIG, BASE_DIR
from middleware.error import error_middleware
from middleware.redis import get_session_middleware
from middleware.user import add_user_middleware
from db.init_db import init_db


async def make_app():
    app = web.Application(
        middlewares=[
            error_middleware,
            await get_session_middleware(),
            add_user_middleware,
        ]
    )

    app["config"] = CONFIG
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates"))
    )

    app.add_routes(people_routes)
    app.add_routes(auth_routes)

    init_db()
    app.cleanup_ctx.append(pg_context)
    return app


web.run_app(make_app(), port=CONFIG.get("APP_PORT"))

# import sys
# print(sys.executable)
