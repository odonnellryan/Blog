import sys
import os
import db_mods
import exception_handling
import views, url_settings, messages
import config_views
from flask import render_template, Flask, g, redirect, url_for
sys.path.append(os.getcwd())

sys.path.append("/usr/share/nginx/www/eztech/public_html")
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(views.mod)
app.register_blueprint(config_views.mod)

@app.context_processor
def inject_urls():
    """
    sets variables that are used in each view. the g-based variables are already passed to the view, so these can
    be factored out, but i left them like this for now.
    """
    return dict(tagged_url=url_settings.tagged_url,preview_post_url=url_settings.preview_post_url)

@app.errorhandler(404)
def page_not_found(e):
    try:
        user_data = db_mods.get_user_data()
    except exception_handling.database_exceptions as e:
        error, redirect_page = exception_handling.database_exception_handler(e)
        user_data = None
        if redirect_page:
            return redirect(url_for(redirect_page))
        return render_template(('404.html'), error_type="MySQL", error_message=error, user_data=user_data)
    if user_data:
        try:
            user_data.tags = user_data.tags.split(',')
        except AttributeError:
            user_data.tags = None
    return render_template('404.html', user_data=user_data, error_message=messages.ERROR_404), 404

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    app.run(port=8000)