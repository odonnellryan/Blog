from config import ADMIN_ID, ADMIN_PASSWORD


def _login(username, password):
    if username == ADMIN_ID and password == ADMIN_PASSWORD:
        return True
    else:
        return False