from __future__ import division
from flask import Blueprint, request, render_template, g, redirect, url_for, session, flash, jsonify, Flask
import decorators
import forms
import blog_mods
import db_mods
import config
from flask_frozen import Freezer
import os
from login import _login, update_password, update_username

mod = Blueprint('blog', __name__, url_prefix='/admin/')

f_mod = Blueprint('f_blog', __name__, url_prefix='/')



@mod.before_request
def before_request():
    g.db = config.DATABASE.connect()
    g.user_data = db_mods.get_user_data()
    g.user_data.tags = g.user_data.tags.split(',')


@mod.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@f_mod.errorhandler(404)
@mod.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="404 Error"), 404


@mod.route('/', methods=['GET', 'POST'])
@decorators.requires_login
def index():
    """admin page"""

    post_mods = {'blog.add' : 'Add a Post', 'blog.delete' : 'Delete a Post', 'blog.edit' : 'Edit Posts',
                   'blog.preview' : 'Preview Main Page', 'blog.commit' : 'Commit your Blog to Flatfile',}

    blog_settings = {'blog.settings' : 'Change Blog Settings', 'blog.change_login': 'Change Login Information'}

    #blog_statistics = {'blog.statistics' : 'View Blog Statistics'}

    return render_template('admin.html', render_html=blog_mods.get_html_content, post_mods=post_mods,
                           blog_settings=blog_settings, user_data=g.user_data)


@mod.route('settings/', methods=['GET', 'POST'])
@decorators.requires_login
def settings():

    """change user defined blog settings from the default"""

    form = forms.BlogSettings(request.form)

    if form.logo_image.data and request.method == 'POST':
        image_data = request.files[form.logo_image.name].read()
        open('/static/imgs/logo.jpg', 'w').write(image_data)

    if not request.method == 'POST':

        current_settings = db_mods.get_user_data()

        form.full_name.data = current_settings.full_name
        form.blog_title.data = current_settings.blog_title
        form.blog_subtitle.data = current_settings.blog_subtitle
        form.footer_text.data = current_settings.footer_text
        form.tags.data = current_settings.tags

    if request.method == 'POST':
        try:
            db_mods.update_all_data(form.blog_title.data, form.blog_subtitle.data, form.full_name.data, form.tags.data,
                                form.footer_text.data)
            flash('Successfully updated user data')
            return redirect(url_for('blog.preview'))
        except Exception, e:
            flash(e)

    return render_template('settings.html', form=form, user_data=g.user_data, page_title="Blog Settings")


@mod.route('settings/change_login/', methods=['GET', 'POST'])
@mod.route('settings/change_login/<validation>', methods=['GET', 'POST'])
@decorators.requires_login
def change_login(validation=None):

    form = forms.ChangeLogin(request.form)

    if form.new_password_1.data:
        if not form.new_password_1.data == form.new_password_2.data:
            flash('Your new passwords do not match. Please try again.')
            return redirect(url_for('blog.change_login'))

    if request.method == 'POST' and _login(form.username.data, form.password.data):
        try:
            if form.new_password_1.data:
                update_password(form.username.data, form.new_password_1.data)
            if form.new_username.data:
                update_username(form.new_username.data)
            flash('Updated your login information.')
            return redirect(url_for('blog.preview'))
        except Exception, e:
            flash('There was an error updating your blog information.' + str(e))
            return render_template('change_login.html')
    elif request.method == 'POST' and not _login(form.username.data, form.password.data):
        flash('Your Current Username or Password Was Incorrect')


    return render_template('change_login.html', form=form, user_data=g.user_data)


@mod.route('preview/', methods=['GET', 'POST'])
@mod.route('preview/<page>/', methods=['GET', 'POST'])
def preview(page=None):

    footer = blog_mods.footer_text()

    if page == 0:
        page = 1
    else:
        try:
            int(page)
        except:
            return redirect(url_for('blog.preview', page=1))

    if int(page) < 0 or not page:
        return redirect(url_for('blog.preview', page=1))
    else:
        posts = db_mods.paginate_visible_posts(int(page))

    page_count = blog_mods.get_number_of_visible_pages()

    pagination = blog_mods.pagination(page, page_count)


    if not pagination['next_page'] == 0:
        next_page = str(pagination['next_page'])
    else:
        next_page = 0

    if not pagination['previous_page'] == 0:
        previous_page = str(pagination['previous_page'])
    else:
        previous_page = 0


    return render_template('preview.html', page=page, posts=posts, render_html=blog_mods.get_html_content, footer=footer,
                           next_page=next_page, previous_page=previous_page, user_data=g.user_data)


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


@mod.route('login/', methods=['GET', 'POST'])
def login():

    form = forms.Login(request.form)

    if request.method == 'POST':
        if _login(form.username.data,form.password.data):
            session['LOGGED_IN'] = True
            return redirect(url_for('blog.index'))
        else:
            flash('Sorry, you put in the wrong information')

    return render_template('login.html', form=form, user_data=g.user_data)


@mod.route('add/', methods=['GET', 'POST'])
@decorators.requires_login
def add():

    form = forms.NewPost(request.form)

    if request.method == 'POST' and form.validate():
        db_mods.add_new_post(form.post_title.data, form.post_body.data)
        return redirect(url_for('blog.preview'))

    return render_template('add.html',  form=form, user_data=g.user_data)


@mod.route('edit/<post_id>/', methods=['GET', 'POST'])
@mod.route('edit/', methods=['GET', 'POST'])
@decorators.requires_login
def edit(post_id=None):

    page_content = []

    form = forms.NewPost(request.form)

    if not post_id:
        page_content = db_mods.get_all_titles_and_ids()

    elif not request.method == 'POST' :
        page_content = db_mods.get_post_content(post_id)
        form.post_title.data = page_content['title']
        form.post_body.data = page_content['body']
        page_content['body_html'] = blog_mods.get_html_content(page_content['body'])

    if request.method == 'POST' and form.validate():
        db_mods.edit_post(form.post_title.data, form.post_body.data, post_id)
        return redirect(url_for('blog.edit'))

    return render_template('edit.html',  form=form, page_content=page_content, post_id=post_id, user_data=g.user_data)


@mod.route('delete/<post_id>', methods=['GET', 'POST'])
@mod.route('delete/', methods=['GET', 'POST'])
@decorators.requires_login
def delete(post_id=None):

    form = forms.Delete(request.form)
    _page_content = db_mods.get_post_content(post_id)

    if not post_id:
        _page_content = db_mods.get_all_titles_and_ids()

    if request.method == 'POST' and form.delete.data:
        _page_content = db_mods.get_post_content(post_id)
        flash('Post successfully deleted: ' + _page_content['title'])
        db_mods.delete_post(post_id)
        return redirect(url_for('blog.index'))

    return render_template('delete.html', page_content=_page_content, post_id=post_id, form=form, user_data=g.user_data)


@mod.route('commit/', methods=['GET', 'POST'])
@decorators.requires_login
def commit():

    f_app = Flask(__name__)
    f_app.register_blueprint(f_mod)
    f_app.testing = True
    f_app.debug = True

    form = forms.Commit(request.form)

    freezer = Freezer(f_app)

    if request.method == 'POST' and form.validate() and form.commit.data == True:
        print freezer.freeze()
        flash('Successfully Committed Your Files')
        return redirect(url_for('blog.index'))

    return render_template('commit.html',  form=form, user_data=g.user_data)


@mod.route('_render_temp_body/', methods=['GET', 'POST'])
def render_temp_body(username=None,article=None):

    try:
        get_markup = blog_mods.get_html_content(request.args.get('post_body'))
        return jsonify(result=get_markup)
    except:
        return("")


@mod.route('_render_temp_title/', methods=['GET', 'POST'])
def render_temp_title():

    try:
        get_markup = request.args.get('post_title')
        return jsonify(result=get_markup)
    except:
        return("")