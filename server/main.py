from aiohttp import web
from routes.routes import setup_routes
from db.db import pg_context
import aiohttp_jinja2
import jinja2
from config.config import CONFIG, BASE_DIR
from middleware.error import error_middleware


app = web.Application(middlewares=[error_middleware])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates")))


setup_routes(app)
app.cleanup_ctx.append(pg_context)


web.run_app(app, port=CONFIG.get("APP_PORT"))

# # import sys
# # print(sys.executable)
