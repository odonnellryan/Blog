import sys

from flask import Flask

from views import mod as blog


sys.path.append("/usr/share/nginx/www/eztech/public_html")
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(blog)



