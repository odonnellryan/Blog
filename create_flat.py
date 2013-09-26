from flask import Blueprint, render_template, Flask
from flask_frozen import Freezer
import _mysql_exceptions
import blog_mods
import db_mods


f_app = Flask(__name__)
f_app.config.from_object('config')
f_mod = Blueprint('f_blog', __name__, url_prefix='/')

tagged_url = 'f_blog.tagged'
preview_url = 'f_blog.generate_blog_pages'
preview_post_url = "f_blog.preview_post"

try :
    user_data = db_mods.get_user_data()
    if user_data.tags :
        user_data.tags = user_data.tags.split(',')
except _mysql_exceptions.OperationalError :
    user_data = None

f_app.debug = True
f_app.testing = True


@f_mod.route('/')
@f_mod.route('<page>/')
def generate_blog_pages(page=1) :
    posts = db_mods.paginate_visible_posts(int(page))
    page_count = blog_mods.get_number_of_visible_pages()
    pagination = blog_mods.pagination(page, page_count)
    if pagination['next_page'] :
        next_page = pagination['next_page']
    else :
        next_page = 0
    if pagination['previous_page'] :
        previous_page = pagination['previous_page']
    else :
        previous_page = 0
    return render_template('preview.html', page=page, posts=posts, render_html=blog_mods.get_html_content,
                           next_page=next_page, previous_page=previous_page, user_data=user_data,
                           tagged_url=tagged_url, preview_url=preview_url, preview_post_url=preview_post_url)


@f_mod.route('tagged/<tag>/', methods=['GET', 'POST'])
@f_mod.route('tagged/', methods=['GET', 'POST'])
def tagged(tag=None) :
    tags = db_mods.tag_array()
    posts = None
    if tag :
        posts = db_mods.search_by_tag(tag)
    return render_template('tagged.html', tags=tags, render_html=blog_mods.get_html_content, user_data=user_data,
                           posts=posts, tagged_url=tagged_url, preview_post_url=preview_post_url)


@f_mod.route('post/<post_id>/', methods=['GET', 'POST'])
def preview_post(post_id=None) :
    page_content = db_mods.get_post_content(post_id)
    return render_template('preview_post.html', page_content=page_content, user_data=user_data,
                           tagged_url=tagged_url, render_html=blog_mods.get_html_content)


@f_mod.route('404.html')
def error_page_not_found() :
    user_data = db_mods.get_user_data()
    if user_data.tags :
        user_data.tags = user_data.tags.split(',')
    return render_template('404.html', user_data=user_data, page_title="404", tagged_url=tagged_url)


f_app.register_blueprint(f_mod)
freezer = Freezer(f_app)