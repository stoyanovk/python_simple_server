from aiohttp import web
from views.people import main_page, create_person, get_people, get_user_people


routes = [
    web.get("/", main_page),
    web.post("/create_person", create_person),
    web.get("/people", get_people),
    web.get("/my-people", get_user_people),
]
