import markdown
from flask import Markup

def get_html_content(get_markdown):
    return Markup(markdown.markdown(get_markdown))