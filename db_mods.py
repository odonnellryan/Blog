import db_config
blog = db_config.RyanBlog


def check_if_title_exists(get_title):
    return blog.where(blog.title == get_title).exists()


def get_all_titles_and_ids():
    posts = {post.post_id : post.title for post in blog.select()}
    return posts


def get_post_content(post_id):
    post = {}
    for _ in blog.select().where(blog.post_id == post_id):
        post['title'] =  _.title
        post['body'] = _.body
    return post

def check_user(get_title, get_user):
    return blog.select().where(blog.title == get_title, blog.username == get_user).exists()


def add_new_post(get_title, get_body):
    blog = db_config.RyanBlog()
    blog.title = get_title
    blog.body = get_body
    blog.save()
    return


def edit_post(get_title, get_body, get_post_id):
    if check_if_title_exists(get_title):
        blog.update(title=get_title, body=get_body).where(blog.post_id == get_post_id)
        blog.execute()
        return True
    return False

