from flask import Blueprint, request, render_template, g, redirect, url_for, session, flash, jsonify, Flask
import decorators
import config
import forms
import blog_mods
import db_mods
from flask_frozen import Freezer


f_app = Flask(__name__)

mod = Blueprint('blog', __name__, url_prefix='/admin/')
f_mod = Blueprint('f_blog', __name__, url_prefix='/')


@mod.route('/', methods=['GET', 'POST'])
@f_mod.route('/', methods=['GET', 'POST'])
def index(article=None, username=None):

    posts = db_mods.get_latest_ten_posts()

    return render_template('view.html', posts=posts, render_html=blog_mods.get_html_content)


@mod.route('admin/', methods=['GET', 'POST'])
@decorators.requires_login
def admin(username=None,article=None):

    return render_template('admin.html')


@mod.route('login/', methods=['GET', 'POST'])
def login(article=None, username=None):

    form = forms.Login(request.form)

    if config._login(form.username.data,form.password.data):
        session['LOGGED_IN'] = True
        return redirect(url_for('blog.add'))
    else:
        flash('Sorry, you put in the wrong information')
    return render_template('login.html', form=form)


@mod.route('add/', methods=['GET', 'POST'])
@decorators.requires_login
def add():

    form = forms.NewPost(request.form)

    if request.method == 'POST' and form.validate():
        db_mods.add_new_post(form.post_title.data, form.post_body.data)
        return redirect(url_for('blog.index'))

    return render_template('add.html',  form=form)


@mod.route('edit/<post_id>/', methods=['GET', 'POST'])
@mod.route('edit/', methods=['GET', 'POST'])
@decorators.requires_login
def edit(post_id=None):

    form = forms.NewPost(request.form)

    if not post_id:
        page_content = db_mods.get_all_titles_and_ids()
    else:
        page_content = db_mods.get_post_content(post_id)
        form.post_title.data = page_content['title']
        form.post_body.data = page_content['body']
        page_content['body_html'] = blog_mods.get_html_content(page_content['body'])

    if request.method == 'POST' and form.validate():
        db_mods.edit_post(form.post_title.data, form.post_body.data, post_id)
        return redirect(url_for('blog.index'))

    return render_template('edit.html',  form=form, page_content=page_content, post_id=post_id)


@mod.route('commit/', methods=['GET', 'POST'])
@decorators.requires_login
def commit(username=None,article=None):

    f_app.register_blueprint(f_mod)

    freezer = Freezer(f_app)

    form = forms.Commit(request.form)

    if request.method == 'POST' and form.validate() and form.commit.data == True:
        freezer.freeze()
        return redirect(url_for('blog.index'))


    return render_template('commit.html',  form=form)


@mod.route('_render_temp_body/', methods=['GET', 'POST'])
def render_temp_body(username=None,article=None):

    try:
        get_markup = blog_mods.get_html_content(request.args.get('post_body'))
        return jsonify(result=get_markup)
    except:
        return("")


@mod.route('_render_temp_title/', methods=['GET', 'POST'])
def render_temp_title(username=None,article=None):

    try:
        get_markup = request.args.get('post_title')
        return jsonify(result=get_markup)
    except:
        return("")


@f_mod.errorhandler(404)
@mod.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="404 Error"), 404