from aiohttp import web

PRIVATE_ROUTES: list[str] = [
    "/my-people",
    "/prayers/create",
    "/prayers/edit",
]


@web.middleware
async def access_control_middleware(request, handler):
    user = request.app.get("user", None)
    if not user and request.path in PRIVATE_ROUTES:
        return web.HTTPFound(location="/login")
    else:
        return await handler(request)
