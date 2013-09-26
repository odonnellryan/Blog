from functools import wraps
from flask import flash, redirect, url_for, session


def requires_login(f) :
    @wraps(f)
    def decorated_function(*args, **kwargs) :
        if not session.get('LOGGED_IN') :
            flash("Sorry, you must be logged in to do this.")
            return redirect(url_for('blog.login'))
        return f(*args, **kwargs)

    return decorated_function