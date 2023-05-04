from aiohttp import web
import jinja2
import aiohttp_jinja2

from routes.people_routes import routes as people_routes
from routes.auth_routes import routes as auth_routes
from routes.prayers_routes import routes as prayers_routes

from config.config import get_config, BASE_DIR
from middleware.error import error_middleware
from middleware.redis import get_session_middleware
from middleware.add_user_middleware import add_user_middleware
from middleware.access_control_middleware import access_control_middleware
from db.init_db import init_db, get_async_session


async def make_app():
    config = get_config()
    app = web.Application(
        middlewares=[
            error_middleware,
            await get_session_middleware(config),
            add_user_middleware,
            access_control_middleware
        ]
    )

    app["config"] = config
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates"))
    )

    app.add_routes(people_routes)
    app.add_routes(auth_routes)
    app.add_routes(prayers_routes)

    await init_db(config)
    app["db"] = get_async_session(config)

    return app


web.run_app(make_app(), port=3001)

# import sys
# print(sys.executable)
