from aiohttp import web
from aiohttp_session import get_session, Session
from typing import Callable


@web.middleware
async def add_user_middleware(request, handler) -> Callable:
    session: Session = await get_session(request)
    request.app["user"] = session.get("user", None)
    return await handler(request)
