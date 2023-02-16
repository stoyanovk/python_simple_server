def get_pagination(page, total, limit):
    pages = list()
    current_page = page
    last_page = round(total / limit)
    neighbor = 1

    if total / limit < 1:
        return pages

    if current_page != 1:
        pages.append({"number": 1})

    if current_page - neighbor - 1 > 1:
        pages.append({"dots": ""})

    if current_page - neighbor > 1:
        pages.append({"number": current_page - 1})

    pages.append({"number": current_page, "is_active": True})

    if current_page + neighbor < last_page:
        pages.append({"number": current_page + 1})

    if last_page > current_page + neighbor + 1:
        pages.append({"dots": ""})

    if current_page + neighbor <= last_page:
        pages.append({"number": last_page})
    return pages
