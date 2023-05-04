from aiohttp import web
from views.prayers_views import (
    create_prayer,
    get_prayers,
    get_prayers_by_id,
    delete_prayer,
    render_create_prayers,
    render_edit_prayers,
    update_prayer,
    assign_prayer,
    get_assigned_prayers
)


routes = [
    web.get("/prayers/assigned", get_assigned_prayers),
    web.get("/prayers", get_prayers),
    web.get("/prayers/create", render_create_prayers),
    web.get("/prayers/edit/{id}", render_edit_prayers),
    web.post("/prayers/create", create_prayer),
    web.get("/prayers/{id}", get_prayers_by_id),
    web.post("/prayers/edit/{id}", update_prayer),
    web.delete("/prayers/{id}", delete_prayer),
    web.post("/prayers/assign/{id}", assign_prayer),
]
