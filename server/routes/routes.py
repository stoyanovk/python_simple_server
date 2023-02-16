from aiohttp import web
from views.views import index, create_name, get_names


def setup_routes(app):
    app.add_routes(
        [
            web.get("/", index),
            web.post("/create_name", create_name),
            web.get("/names", get_names),
        ]
    )
