import markdown
from flask import Markup, redirect, url_for
import db_mods


def get_html_content(get_markdown):
    return Markup(markdown.markdown(get_markdown))


def get_number_of_visible_pages():
    post_count = db_mods.get_visible_post_count()
    if (post_count % 10) == 0:
        return post_count / 10
    else:
        return (post_count / 10) + 1


def pagination(current_page, total_pages):
    """
    :param current_page: what page the user is currently on
    :param total_pages: how many pages they are
    :return: pagination, a dict with 'previous_page' and 'next_page' keys
            the keys would be 0 if there is no next or previous page
    """
    try:
        current_page = int(current_page)
    except ValueError:
        pass
    try:
        total_pages = int(total_pages)
    except ValueError:
        pass
    pagination = {}
    if current_page == None and total_pages > 1:
        next_page = 2
    elif current_page == None and total_pages <= 1:
        next_page = 0
    elif current_page < total_pages:
        next_page = current_page + 1
    else:
        next_page = 0
    pagination['next_page'] = next_page
    if total_pages > 1 and current_page <= total_pages and current_page > 0:
        previous_page = current_page - 1
    else:
        previous_page = 0
    pagination['previous_page'] = previous_page
    return pagination


def get_page_numbers(page):
    page_count = get_number_of_visible_pages()
    get_pagination = pagination(page, page_count)
    if not get_pagination['next_page'] == 0:
        next_page = str(get_pagination['next_page'])
    else:
        next_page = 0
    if not get_pagination['previous_page'] == 0:
        previous_page = str(get_pagination['previous_page'])
    else:
        previous_page = 0
    return previous_page, next_page


def fix_page_values(page):
    try:
        page_value = int(page)
        if page_value < 1:
            page_value = 0
    except ValueError:
        page_value = 0
    return page_value