from dataclasses import dataclass


@dataclass
class Button:
    number: int | None = None
    dots: bool = False
    is_active: bool = False


Buttons = list[Button]


def get_pagination(page: int, total: int, limit: int) -> Buttons:
    pages: Buttons = list()
    current_page: int = page

    last_page: int | float = total / limit
    neighbor: int = 1
    if total / limit < 1:
        return pages

    if current_page != 1:
        pages.append(Button(1))

    if current_page - neighbor - 1 > 1:
        pages.append(Button(dots=True))

    if current_page - neighbor > 1:
        pages.append(Button(current_page - 1))

    pages.append(Button(current_page, is_active=True))

    if current_page + neighbor < last_page:
        pages.append(Button(current_page + 1))

    if last_page > current_page + neighbor + 1:
        pages.append(Button(dots=True))

    if current_page + neighbor <= last_page:
        pages.append(Button(round(last_page)))
    return pages
