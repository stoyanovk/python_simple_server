from dataclasses import dataclass


@dataclass
class Button:
    number: int = None
    dots: bool = False
    is_active: bool = False


def get_pagination(page, total, limit):
    pages = list()
    current_page = page
    last_page = round(total / limit)
    neighbor = 1

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
        pages.append(Button(last_page))
    return pages
