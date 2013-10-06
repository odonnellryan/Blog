import sys
import os
import db_mods
import views, url_settings, messages
from flask import render_template, Flask, g
sys.path.append(os.getcwd())

sys.path.append("/usr/share/nginx/www/eztech/public_html")
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(views.mod)

@app.context_processor
def inject_urls():
    """
    sets variables that are used in each view. the g-based variables are already passed to the view, so these can
    be factored out, but i left them like this for now.
    """
    return dict(tagged_url=url_settings.tagged_url,preview_post_url=url_settings.preview_post_url)

@app.errorhandler(404)
def page_not_found(e):
    user_data = db_mods.get_user_data()
    if user_data.tags:
        user_data.tags = user_data.tags.split(',')
    return render_template('404.html', user_data=user_data, error_message=messages.ERROR_404), 404

app.testing = True
#TODO: turn debugging off
app.debug = True

if __name__ == '__main__':
    app.run(port=8000)