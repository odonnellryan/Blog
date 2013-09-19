from flask import Flask, render_template
import db_mods
import sys
from views import mod as blog

sys.path.append("/usr/share/nginx/www/eztech/public_html")
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(blog)



