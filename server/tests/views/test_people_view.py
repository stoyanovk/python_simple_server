import pytest

# from aiohttp import web
from unittest.mock import MagicMock

from views.people_view import main_page

request = MagicMock()


@pytest.mark.asyncio
async def test_main_page():

    request.app = {"user": {'id': 1, 'name': 'TEST'}}

    result = await main_page(request=request)
    print(result)
