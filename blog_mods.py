import markdown
from flask import Markup
import db_mods

def get_html_content(get_markdown):
    return Markup(markdown.markdown(get_markdown))


def footer_text():
    return "This is your footer-text"


def get_number_of_visible_pages():
        post_count = db_mods.get_visible_post_count()
        if (post_count % 10) == 0:
            return post_count / 10
        else:
            return (post_count / 10) + 1


def pagination(current_page, total_pages):

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