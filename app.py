from flask import request, render_template, flash, Flask, g, session, url_for
import sys
import config


sys.path.append("/usr/share/nginx/www/eztech/public_html")


app = Flask(__name__)

app.config.from_object('config')

from views import mod as blog

app.register_blueprint(blog)
