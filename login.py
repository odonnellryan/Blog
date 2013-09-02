import db_config
import db_mods
from passlib.apps import custom_app_context as pwd_context

user_d = db_config.UserData

def update_password(get_username, get_password):
    password = pwd_context.encrypt(get_password)
    update = user_d.update(password=password).where(user_d.username == get_username)
    update.execute()

def update_username(get_username):
    tags = user_d.update(username=get_username).where(user_d.id == 0)
    tags.execute()


def _login(username, password):

    try:
        _hash = db_mods.get_password(username)
    except:
        return False

    if pwd_context.verify(password, _hash):
        return True

    return False