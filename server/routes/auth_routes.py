from aiohttp import web
from views.auth_view import register_page, login_page, create_user, login, logout

routes = [
    web.get("/register", register_page),
    web.get("/login", login_page),
    web.get("/logout", logout),
    web.post("/create", create_user),
    web.post("/login", login),
]
