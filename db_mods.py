import db_config
blog = db_config.RyanBlog


def check_if_title_exists(get_title):
    return blog.where(blog.title == get_title).exists()


def check_user(get_title, get_user):
    return blog.select().where(blog.title == get_title, blog.username == get_user).exists()


def add_new_post(get_title, get_body):
    blog = db_config.RyanBlog()
    blog.title = get_title
    blog.content = get_body
    blog.save()
    return True


def edit_post(get_title, get_body, get_user):
    if check_if_title_exists(get_title):
        blog.update(title=get_title, content=get_body, username=get_user).where(blog.title == get_title)
        blog.execute()
        return True
    return False