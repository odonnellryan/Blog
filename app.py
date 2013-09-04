from flask import Flask, render_template
import db_mods
import sys
from views import mod as blog

sys.path.append("/usr/share/nginx/www/eztech/public_html")
app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(blog)

@app.errorhandler(404)
def page_not_found(e):
    user_data = db_mods.get_user_data()
    user_data.tags = user_data.tags.split(',')
    return render_template('404.html', user_data=user_data), 404

