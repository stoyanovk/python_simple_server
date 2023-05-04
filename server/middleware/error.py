from aiohttp import web
import aiohttp_jinja2


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response

    except Exception as err:
        if isinstance(err, web.HTTPError):
            return aiohttp_jinja2.render_template(
                "error-page.html", request, {"error": err.reason}, status=404
            )
        else:
            return aiohttp_jinja2.render_template(
                "error-page.html", request, {"error": err}, status=404
            )
