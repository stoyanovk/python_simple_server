from aiohttp import web
import aiohttp_jinja2


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)

        if response.status < 400:
            return response

    except web.HTTPPaymentRequired as err:
        print(err, "error")

    return aiohttp_jinja2.render_template(
        "error-page.html", request, {"error": response.reason}, status=404
    )
