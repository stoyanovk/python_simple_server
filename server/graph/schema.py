import strawberry

from aiohttp import web
from strawberry.aiohttp.views import GraphQLView

from graph.user_graph import users, user, User
from graph.prayer_graph import prayer, prayers, Prayer, assigned_prayers
from graph.people_praph import people, person, People


class MyGraphQLView(GraphQLView):
    async def get_context(self, request: web.Request, response: web.StreamResponse):
        return {"request": request, "response": response}


@strawberry.type
class Query:
    users: list[User] = strawberry.field(resolver=users)
    user: User | None = strawberry.field(resolver=user)
    prayer: Prayer | None = strawberry.field(resolver=prayer)
    prayers: list[Prayer] = strawberry.field(resolver=prayers)
    people: list[People] = strawberry.field(resolver=people)
    person: People | None = strawberry.field(resolver=person)
    assigned_prayers: list[Prayer] = strawberry.field(resolver=assigned_prayers)


schema = strawberry.Schema(query=Query)
