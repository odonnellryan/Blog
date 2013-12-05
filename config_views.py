from flask import Blueprint, redirect, url_for, flash, request, render_template
import db_structure
import db_mods
from exception_handling import database_exceptions
import forms
import messages
import image_mods
import login

mod = Blueprint('config', __name__, url_prefix='/config/')

@mod.route('database/tables/', methods=['GET', 'POST'])
def db_tables(tag=None):

    user_data_form = forms.BlogSettings(request.form)

    login_form = forms.SetLogin(request.form)

    try:
        db_mods.get_user_data()
        return redirect(url_for('blog.index'))

    except database_exceptions as e:
        #just a safety to ensure this can only be run if this is thrown (aka, this is the table-not-existing thing)
        if 1146 in e.args:
            if request.method == 'POST' and login_form.validate():
                image_mods.image_tool_logo(request.files)
                db_structure.UserData.create_table()
                db_structure.Posts.create_table()
                try:
                    login.set_login_details(login_form.username.data, login_form.password.data, login_form.confirm_password.data)
                except ValueError:
                    flash(messages.ERROR_USER_ALREADY_CONFIGURED)
                db_mods.update_all_data(user_data_form.blog_title.data, user_data_form.blog_subtitle.data,
                                        user_data_form.full_name.data, user_data_form.tags.data,
                                        user_data_form.footer_text.data)
                flash(messages.MESSAGE_UPDATED_DATA)
                return redirect(url_for('blog.index'))

            return render_template('install.html', user_data_form=user_data_form, login_form=login_form, error_type="Install Mysql",
                           error_message='improper_tables', user_data=None)
    return redirect(url_for('blog.index'))