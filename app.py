from flask import request, render_template, flash, Flask, g, session, url_for
import sys
import config
from flask_frozen import Freezer


sys.path.append("/usr/share/nginx/www/eztech/public_html")


app = Flask(__name__)
f_app = Flask(__name__)
app.config.from_object('config')

from views import mod as blog
from views import f_mod as f_blog


app.register_blueprint(blog)

f_app.register_blueprint(f_blog)

freezer = Freezer(f_app)

@f_app.errorhandler(404)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="404 Error"), 404