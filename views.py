from flask import Blueprint, request, render_template, g, redirect, url_for, session, flash, jsonify

from db_config import RyanBlog
import decorators
import config
import forms
import blog_mods
import db_mods
from subprocess import call

mod = Blueprint('blog', __name__, url_prefix='/')
f_mod = Blueprint('f_blog', __name__, url_prefix='/')

@mod.route('/', methods=['GET', 'POST'])
@f_mod.route('/', methods=['GET', 'POST'])
def index(article=None, username=None):
    blog_posts = RyanBlog.select()

    posts = [post for post in blog_posts.order_by(RyanBlog.post_id.desc()).limit(10)]

    return render_template('view.html', posts=posts, render_html=blog_mods.get_html_content)


@mod.route('login/', methods=['GET', 'POST'])
@f_mod.route('/', methods=['GET', 'POST'])
def login(article=None, username=None):
    form = forms.Login(request.form)
    if config._login(form.username.data,form.password.data):
        session['LOGGED_IN'] = True
        return redirect(url_for('blog.add'))

    else:
        print config._login(form.username.data,form.password.data)
        flash('Sorry, you put in the wrong information' + str(form.username.data) + str(form.password.data))

    return render_template('login.html', form=form)


@mod.route('add/', methods=['GET', 'POST'])
@decorators.requires_login
def add(username=None,article=None):

    form = forms.NewPost(request.form)

    if request.method == 'POST' and form.validate():
        db_mods.add_new_post(form.post_title.data, form.post_body.data)
        return redirect(url_for('blog.index'))

    return render_template('add.html',  form=form)


@mod.route('commit/', methods=['GET', 'POST'])
@decorators.requires_login
def commit(username=None,article=None):

    form = forms.Commit(request.form)

    if request.method == 'POST' and form.validate() and form.commit.data == True:
        call('python run.py build')
        flash('Committed your changes to Flat Files')

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

