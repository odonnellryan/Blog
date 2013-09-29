from passlib.apps import custom_app_context as pwd_context
import _mysql_exceptions
import db_config
import db_mods


user_d = db_config.UserData


def update_password(get_username, get_password):
    password = pwd_context.encrypt(get_password)
    update = user_d.update(password=password).where(user_d.username == get_username)
    update.execute()


def update_password_no_username(get_password):
    password = pwd_context.encrypt(get_password)
    update = user_d.update(password=password).where(user_d.id == 0)
    update.execute()


def update_username(get_username):
    tags = user_d.update(username=get_username).where(user_d.id == 0)
    tags.execute()


def update_email(get_new_email):
    query = user_d.update(email=get_new_email).where(user_d.id == 0)
    query.execute()


def user_login(username, password):
    try:
        _hash = db_mods.get_password(username)
    except _mysql_exceptions.OperationalError:
        return False

    if pwd_context.verify(password, _hash):
        return True

    return False