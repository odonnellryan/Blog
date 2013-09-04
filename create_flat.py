from flask import Blueprint, render_template, Flask
import blog_mods
import db_mods
from flask_frozen import Freezer

f_app = Flask(__name__)
f_app.config.from_object('config')
f_mod = Blueprint('f_blog', __name__, url_prefix='/')


@f_mod.route('/')
@f_mod.route('<page>/')
def generate_blog_pages(page=1):

    user_data = db_mods.get_user_data()
    user_data.tags = user_data.tags.split(',')

    posts = db_mods.paginate_visible_posts(int(page))

    page_count = blog_mods.get_number_of_visible_pages()

    pagination = blog_mods.pagination(page, page_count)

    if not pagination['next_page'] == 0:
        next_page = pagination['next_page']
    else:
        next_page = 0


    if not pagination['previous_page'] == 0:
        previous_page = pagination['previous_page']
    else:
        previous_page = 0

    return render_template('generate.html', page=page, posts=posts, render_html=blog_mods.get_html_content,
                           next_page=next_page, previous_page=previous_page, user_data=user_data)


@f_mod.route('/404.html')
def error_page_not_found():
    return render_template('404.html')


f_app.register_blueprint(f_mod)
freezer = Freezer(f_app)