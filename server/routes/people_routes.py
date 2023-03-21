from aiohttp import web
from views.people_view import (
    main_page,
    create_person,
    get_people,
    get_user_people,
    get_leader_board,
)


routes = [
    web.get("/", main_page),
    web.post("/create_person", create_person),
    web.get("/people", get_people),
    web.get("/my-people", get_user_people),
    web.get("/people/leader-board", get_leader_board),
]
