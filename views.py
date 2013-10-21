from __future__ import division
from collections import OrderedDict
from flask import Blueprint, request, render_template, g, redirect, url_for, session, flash, jsonify
from wtforms import BooleanField
from login import user_login, update_password, update_username
from peewee import DoesNotExist
import url_settings
import decorators
import forms
import blog_mods
import db_mods
import config
import create_flat
import helper_funcs
import image_mods
import messages
import _mysql_exceptions


mod = Blueprint('blog', __name__, url_prefix='/admin/')

@mod.before_request
def before_request():
    """
        before request
        gets the user information from the DB to pass to the pages
        checks if session is set for login
    """
    try:
        g.db = config.DATABASE.connect()
        g.user_data = db_mods.get_user_data()
        if g.user_data.tags:
            g.user_data.tags = g.user_data.tags.split(',')
        try:
            g.logged_in = session['LOGGED_IN']
        except KeyError:
            g.logged_in = False
    except _mysql_exceptions.OperationalError, e:
        g.logged_in = False
        g.user_data = False
        #check if it's an auth error (in this case most likely db info isn't set correctly)
        if 1045 in e.args:
            return render_template('404.html', error_type="MySQL", error_message=messages.ERROR_DATABASE_CONFIGURATION)
        #check if there is any database configuration stuff. if there is not, redirect to the install page
        if not config.DATABASE:
            return render_template('install.html', error_type="MySQL", error_message=messages.ERROR_DATABASE_CONNECTION)
        return render_template('404.html', error_type="MySQL", error_message=messages.ERROR_DATABASE_CONNECTION)

@mod.context_processor
def inject_urls():
    """
        sets variables that are used in each view. the g object is already passed to the view, so these can
        be factored out, but i left them like this for now.
    """

    #try block is to handle errors related to mysql connection, etc. g.userdata not defined if database doesn't connect
    try:
        if g.user_data.footer_text:
            g.user_data.footer_text = blog_mods.get_html_content(g.user_data.footer_text)
    except AttributeError:
        pass
    if g.user_data:
        user_data = g.user_data
        logged_in = g.logged_in
        page_title = user_data.blog_subtitle
    else:
        user_data = None
        logged_in = None
        page_title = None
    return dict(tagged_url=url_settings.tagged_url, preview_url=url_settings.preview_url,
            preview_post_url=url_settings.preview_post_url, render_html=blog_mods.get_html_content,
            user_data=user_data, logged_in=logged_in,page_title=page_title)

@mod.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@mod.route('/', methods=['GET', 'POST'])
@decorators.requires_login
def index():
    """
        admin and flask-site landing page
    """
    total_count = str(db_mods.get_total_post_count())
    draft_count = str(db_mods.get_draft_post_count())
    published_count = str(db_mods.get_visible_post_count())

    post_mods = OrderedDict([('blog.add_images', 'Add a Post'),
                             ('blog.delete', " ".join(("Delete a Post (", published_count, ")"))),
                             ('blog.edit', 'Edit Posts'),
                             ('blog.commit', 'Commit your Blog to Flatfile')])

    blog_settings = OrderedDict([('blog.settings', 'Change Blog Settings'),
                                 ('blog.change_login', 'Change Login Information')])

    view_posts = OrderedDict([('blog.drafts', " ".join(("View Drafts (", draft_count, ")"))),
                             ('blog.preview', 'Preview Main Page')])

    #blog_statistics = {'blog.statistics': 'View Blog Statistics'}  #future statistics page

    return render_template('admin.html', post_mods=post_mods, blog_settings=blog_settings, view_posts=view_posts,
                           total_count=total_count, draft_count=draft_count, published_count=published_count)

@mod.route('settings/', methods=['GET', 'POST'])
@decorators.requires_login
def settings():
    """
        change user defined blog settings from the default
    """

    form = forms.BlogSettings(request.form)

    if not request.method == 'POST':
        current_settings = db_mods.get_user_data()
        form.full_name.data = current_settings.full_name
        form.blog_title.data = current_settings.blog_title
        form.blog_subtitle.data = current_settings.blog_subtitle
        form.footer_text.data = current_settings.footer_text
        form.tags.data = current_settings.tags

    if request.method == 'POST' and form.validate():
        image_mods.image_tool_logo(request.files)
        db_mods.update_all_data(form.blog_title.data, form.blog_subtitle.data, form.full_name.data, form.tags.data,
                                form.footer_text.data)
        flash(messages.MESSAGE_UPDATED_DATA)
        return redirect(url_for('blog.preview'))

    return render_template('settings.html', form=form, page_title="Blog Settings")

@mod.route('settings/change_login/', methods=['GET', 'POST'])
@decorators.requires_login
def change_login():
    form = forms.ChangeLogin(request.form)
    if form.new_password_1.data:
        if not form.new_password_1.data == form.new_password_2.data:
            flash(messages.ERROR_PASSWORDS_DONT_MATCH)
            return redirect(url_for('blog.change_login'))
    if request.method == 'POST' and user_login(form.username.data, form.password.data):
        try:
            if form.new_password_1.data:
                update_password(form.username.data, form.new_password_1.data)
            if form.new_username.data:
                update_username(form.new_username.data)
            flash(messages.MESSAGE_UPDATED_DATA)
            return redirect(url_for('blog.preview'))
        except Exception, e:
            flash(messages.ERROR_UPDATING_INFO + messages.ERROR_CODE_RETURN(str(e)))
            return render_template('change_login.html')
    elif request.method == 'POST' and not user_login(form.username.data, form.password.data):
        flash('Your Current Username or Password was incorrect')
    return render_template('change_login.html', form=form, page_title="Change Login Information")

@mod.route('preview/', methods=['GET', 'POST'])
@mod.route('preview/<page>/', methods=['GET', 'POST'])
@decorators.requires_login
def preview(page=None):
    page_number = blog_mods.fix_page_values(page)
    if page_number == 0 or not page:
        return redirect(url_for('blog.preview', page=1))
    else:
        posts = db_mods.paginate_visible_posts(page_number)
    if not posts.count():
        posts = None
    previous_page, next_page = blog_mods.get_page_numbers(page)
    return render_template('preview.html', page=page, posts=posts, next_page=next_page, previous_page=previous_page)

@mod.route('posts/', methods=['GET', 'POST'])
@mod.route('posts/<page>/', methods=['GET', 'POST'])
@decorators.requires_login
def posts(page=None):
    """
        eventually will display a page that has links next to the post to "unpublish, edit, delete, publish, copy" etc
        to help with administration
    """
    page_number = blog_mods.fix_page_values(page)
    if page_number == 0 or not page:
        return redirect(url_for('blog.posts', page=1))
    else:
        posts = db_mods.paginate_visible_posts(page_number)
    previous_page, next_page = blog_mods.get_page_numbers(page)
    return render_template('posts.html', page=page, posts=posts, next_page=next_page, previous_page=previous_page)

@mod.route('preview/tagged/<tag>', methods=['GET', 'POST'])
@mod.route('preview/tagged/', methods=['GET', 'POST'])
@decorators.requires_login
def tagged(tag=None):
    if tag:
        posts = db_mods.search_by_tag(tag)
        if not posts.count():
            posts = None
        return render_template('preview.html', posts=posts, page_title=tag)
    return redirect(url_for('blog.preview', page=1))

@mod.route('preview/post/<post_id>/<post_title>/', methods=['GET', 'POST'])
@mod.route('preview/post/<post_id>/', methods=['GET', 'POST'])
@decorators.requires_login
def preview_post(post_id=None, post_title=None):
    if not db_mods.check_if_post_exists(post_id):
        flash(messages.ERROR_POST_DOES_NOT_EXIST)
        return redirect(url_for('blog.preview'))
    page_content = db_mods.get_post_content(post_id)
    if not post_title:
        redirect(url_for('blog.preview_post', post_id=post_id, post_title=page_content['url_title']))
    return render_template('preview_post.html', page_content=page_content, page_title=page_content['title'])

@mod.route('drafts/', methods=['GET', 'POST'])
@mod.route('drafts/<page>/', methods=['GET', 'POST'])
@decorators.requires_login
def drafts(page=None):
    """
        the view page for the drafts
    """
    page_number = blog_mods.fix_page_values(page)
    if page_number == 0 or not page:
        return redirect(url_for('blog.drafts', page=1))
    else:
        posts = db_mods.paginate_drafts(page_number)
    if not posts.count():
        posts = None
    previous_page, next_page = blog_mods.get_page_numbers(page)
    return render_template('posts.html', page=page, posts=posts, next_page=next_page, previous_page=previous_page)

@mod.route('login/', methods=['GET', 'POST'])
def login():
    if g.logged_in:
        return redirect(url_for('blog.index'))
    form = forms.Login(request.form)
    if request.method == 'POST' and form.validate():
        try:
            if user_login(form.username.data, form.password.data):
                session['LOGGED_IN'] = True
                return redirect(url_for('blog.index'))
            else:
                flash(messages.ERROR_USER_INFO_INCORRECT)
        except DoesNotExist:
            flash(messages.ERROR_USER_INFO_INCORRECT)
    return render_template('login.html', form=form, page_title="Login")

@mod.route('forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@mod.route('logout/', methods=['GET', 'POST'])
@decorators.requires_login
def logout():
    session.pop('LOGGED_IN')
    return redirect("/")

@mod.route('add/images/', methods=['GET', 'POST'])
@decorators.requires_login
def add_images():
    """
    add images page
    """
    if request.method == 'POST':
        image_list = image_mods.call_image_tool_posts(request.files)
        post_id = db_mods.add_new_post('Post Title', 'Post Body', [], image_mods.array_to_comma_list(image_list))
        return redirect(url_for('blog.edit', post_id=post_id))
    return render_template('add_images.html', page_title="Add a new post")

@mod.route('add/post/', methods=['GET', 'POST'])
@decorators.requires_login
def add_post():
    post_id = db_mods.add_new_post('Post Title', 'Post Body', [])
    return redirect(url_for('blog.edit', post_id=post_id))

#can probably make this a lot cleaner..
@mod.route('edit/<post_id>/', methods=['GET', 'POST'])
@mod.route('edit/', methods=['GET', 'POST'])
@decorators.requires_login
def edit(post_id=None):
    form = []
    page_content = []
    images = []
    current_tags = []
    post_tags = []
    image_tagged_values = []
    tag_values = []
    if post_id:
        class NewPostTags(forms.NewPost):
            pass
        post_tags = db_mods.tag_array()
        if post_tags:
            for name in post_tags:
                setattr(NewPostTags, name, BooleanField(name))
        try:
            image_array = image_mods.image_array(post_id)
        except DoesNotExist:
            flash(messages.ERROR_POST_DOES_NOT_EXIST)
            return redirect(url_for('blog.edit'))
        if image_array:
            for im_name in image_array:
                setattr(NewPostTags, im_name, BooleanField(""))
        form = NewPostTags(request.form)
        if post_tags:
            tag_values = helper_funcs.return_method_dict(form, post_tags)
        if image_array:
            image_tagged_values = helper_funcs.return_method_dict(form, image_array)
    if not post_id:
        page_content = db_mods.get_all_visible_titles_and_ids()
        page_title = "Edit a Post"
    elif not request.method == 'POST' and post_id:
        page_content = db_mods.get_post_content(post_id)
        page_title = "Edit Post: " + page_content['title']
        form.post_title.data = page_content['title']
        form.post_body.data = page_content['body']
        current_tags = page_content['tags']
        # checks the checkbox if the tag is attached to the post
        if post_tags and current_tags:
            for tag in current_tags:
                if tag in tag_values:
                    tag_values[tag].data = 'y'
        images = page_content['images']
        page_content['body_html'] = blog_mods.get_html_content(page_content['body'])
    if request.method == 'POST':
        if image_tagged_values:
            image_mods.remove_images(post_id, image_tagged_values)
        uploaded_images = image_mods.array_to_comma_list(image_mods.call_image_tool_posts(request.files))
        current_images = image_mods.array_to_comma_list(image_mods.image_array(post_id))
        image_list = []
        if uploaded_images:
            image_list.append(uploaded_images)
        if current_images:
            image_list.append(current_images)
        image_list = image_mods.array_to_comma_list(image_list)
        if 'SavePublish' in request.form:
            db_mods.edit_post(form.post_title.data, form.post_body.data, post_id, tag_values, image_list, published=True)
            return redirect(url_for(url_settings.preview_url))
        db_mods.edit_post(form.post_title.data, form.post_body.data, post_id, tag_values, image_list)
        return redirect(url_for('blog.index'))
    return render_template('edit.html', form=form, page_content=page_content, post_id=post_id,
                           tag_values=tag_values, images=images, tagged=current_tags, image_tags=image_tagged_values,
                           page_title=page_title)

@mod.route('delete/<post_id>', methods=['GET', 'POST'])
@mod.route('delete/', methods=['GET', 'POST'])
@decorators.requires_login
def delete(post_id=None):
    form = forms.Delete(request.form)
    _page_content = db_mods.get_post_content(post_id)
    if not post_id:
        _page_content = db_mods.get_all_visible_titles_and_ids()
    if request.method == 'POST' and form.delete.data:
        current_images = image_mods.image_array(post_id)
        image_mods.delete_images(current_images, current_images)
        _page_content = db_mods.get_post_content(post_id)
        flash(messages.MESSAGE_POST_DELETED(_page_content['title']))
        db_mods.delete_post(post_id)
        return redirect(url_for('blog.index'))
    if request.method == 'POST' and not form.delete.data:
        flash(messages.ERROR_ACTION_NOT_CONFIRMED)
    return render_template('delete.html', page_content=_page_content, post_id=post_id, form=form,
                           page_title="Delete a Post")

@mod.route('commit/', methods=['GET', 'POST'])
@decorators.requires_login
def commit():
    form = forms.Commit(request.form)

    if request.method == 'POST':
        if form.commit.data == True:
            create_flat.freezer.freeze()
            flash('Successfully Committed Your Files')
            return redirect(url_for('blog.index'))
        else:
            flash("Please click Commit to Flat Files if you wish to Commit your changes.")
            return redirect(url_for('blog.commit'))

    return render_template('commit.html', form=form, page_title="Commit your blog to Flatfile")

#below are the two views to work with jquery. these views process the text, html, and markup to produce valid html
#can probably use one of these rather than two..
@mod.route('_render_temp_body/', methods=['GET', 'POST'])
def render_temp_body(username=None, article=None):
    if request.args.get('post_body'):
        get_markup = blog_mods.get_html_content(request.args.get('post_body'))
        return jsonify(result=get_markup)

@mod.route('_render_temp_title/', methods=['GET', 'POST'])
def render_temp_title():
    if request.args.get('post_title'):
        get_markup = request.args.get('post_title')
        return jsonify(result=get_markup)

