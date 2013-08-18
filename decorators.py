from functools import wraps
from flask import g, flash, redirect, url_for, request, session

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Sorry, you must be logged in to do this.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function