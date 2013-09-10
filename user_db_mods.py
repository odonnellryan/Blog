from db_mods import user_d


def email_username_check(get_email, get_username):
    try:
        if user_d.get(user_d.email == get_email, user_d.username == get_username):
            return True
    except Exception, e:
        return False


def return_username():
    query = user_d.get(user_d.id == 0)
    return query.username


def match_auth_string(get_username, get_email, get_auth_string):
    try:
        if user_d.get(user_d.username == get_username, user_d.email == get_email,
                      user_d.forgot_password == get_auth_string).id == 0:
            return True
    except:
        return False

