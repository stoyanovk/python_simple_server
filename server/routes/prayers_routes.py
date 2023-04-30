from aiohttp import web
from views.prayers_views import (
    create_prayer,
    get_prayers,
    get_prayers_by_id,
    delete_prayer,
    render_create_prayers,
    render_edit_prayers
)


routes = [
    web.get("/prayers", get_prayers),
    web.get("/prayers/create", render_create_prayers),
    web.get("/prayers/edit/{id}", render_edit_prayers),
    web.get("/prayers/{id}", get_prayers_by_id),
    web.post("/prayers/create", create_prayer),
    web.put("/prayers/edit/{id}", create_prayer),
    web.delete("/prayers/{id}", delete_prayer),
]
