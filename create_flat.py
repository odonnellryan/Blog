from flask import Blueprint, render_template, Flask, redirect, url_for
from flask_frozen import Freezer
import blog_mods
import db_mods
import exception_handling

f_app = Flask(__name__)
f_app.config.from_object('config')
f_mod = Blueprint('f_blog', __name__, url_prefix='/')

tagged_url = 'f_blog.tagged'
preview_url = 'f_blog.generate_blog_pages'
preview_post_url = "f_blog.preview_post"



f_app.debug = True
f_app.testing = True

@f_mod.context_processor
def inject_urls():
    """
        sets variables that are used in each view. the g object is already passed to the view, so these can
        be factored out, but i left them like this for now.
    """
    try:
        user_data = db_mods.get_user_data()
        if user_data.tags:
            user_data.tags = user_data.tags.split(',')
    except exception_handling.database_exceptions:
        user_data = None

    user_data.footer_text = blog_mods.get_html_content(user_data.footer_text)
    return dict(tagged_url=tagged_url, preview_url=preview_url,preview_post_url=preview_post_url, user_data=user_data,
                render_html=blog_mods.get_html_content, page_title=user_data.blog_subtitle)


@f_mod.route('/')
@f_mod.route('<page>/')
def generate_blog_pages(page=1):
    page_number = blog_mods.fix_page_values(page)
    posts = db_mods.paginate_visible_posts(page_number)
    if not posts.count():
        posts = None
    previous_page, next_page = blog_mods.get_page_numbers(page)
    return render_template('preview.html', page=page, posts=posts, next_page=next_page, previous_page=previous_page)


@f_mod.route('tagged/<tag>/', methods=['GET', 'POST'])
@f_mod.route('tagged/', methods=['GET', 'POST'])
def tagged(tag=None):
    posts = None
    if tag:
        posts = db_mods.search_by_tag(tag)
    return render_template('preview.html', posts=posts, page_title=tag)


@f_mod.route('post/<post_id>/<post_title>/', methods=['GET', 'POST'])
@f_mod.route('post/<post_id>/', methods=['GET', 'POST'])
def preview_post(post_id=None, post_title=None):
    page_content = db_mods.get_post_content(post_id)
    if not post_title:
        title = page_content['url_title']
        redirect(url_for('f_blog.preview_post', post_id=post_id, post_title=title))
    return render_template('preview_post.html', page_content=page_content, page_title=page_content['title'])


@f_mod.route('404.html')
def error_page_not_found():
    user_data = db_mods.get_user_data()
    if user_data.tags:
        user_data.tags = user_data.tags.split(',')
    return render_template('404.html', page_title="404")


f_app.register_blueprint(f_mod)
freezer = Freezer(f_app)