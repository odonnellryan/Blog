from passlib.apps import custom_app_context as pwd_context
import _mysql_exceptions
import db_structure
import db_mods

user_d = db_structure.UserData

def user_login(username, password):
    try:
        _hash = db_mods.get_password(username)
    except _mysql_exceptions.OperationalError:
        return False
    if pwd_context.verify(password, _hash):
        return True
    return False

def update_login_details(get_username, get_password, set_username=None, set_password=None, confirm_password=None):
    if set_password is not confirm_password:
        return False
    if user_login(get_username, get_password):
        if set_username:
            query = user_d.update(username=set_username).where(user_d.username == get_username)
            query.execute()
            get_username = set_username
        if set_password:
            password = pwd_context.encrypt(set_password)
            query = user_d.update(password=password).where(user_d.username == get_username)
            query.execute()

def set_login_details(set_username, set_password, confirm_password):
    if set_password == confirm_password:
        print set_username, set_password, confirm_password
        password = pwd_context.encrypt(set_password)
        query = user_d()
        query.username = set_username
        query.password = password
        query.save()

#print set_login_details('test', 'test', 'test')