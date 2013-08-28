import db_config
blog = db_config.blog


def check_if_post_exists(get_post_id):
    return blog.select().where(blog.post_id == get_post_id).exists()


def get_all_titles_and_ids():
    posts = {post.post_id : post.title for post in blog.select()}
    return posts


def get_latest_ten_posts():
    blog_posts = blog.select()
    posts = [post for post in blog_posts.order_by(blog.post_id.desc()).limit(10)]
    return posts


def get_post_content(post_id):
    post = {}
    for _ in blog.select().where(blog.post_id == post_id):
        post['title'] = _.title
        post['body'] = _.body
    return post


def check_user(get_title, get_user):
    return blog.select().where(blog.title == get_title, blog.username == get_user).exists()


def add_new_post(get_title, get_body):
    insert_blog = blog()
    insert_blog.title = get_title
    insert_blog.body = get_body
    insert_blog.save()
    return


def edit_post(get_title, get_body, get_post_id):
    if check_if_post_exists(get_post_id):
        blog.update(title=get_title, body=get_body).where(blog.post_id == get_post_id)
        blog.execute()
        return True
    return False


def delete_post(get_post_id):
    if check_if_post_exists(get_post_id):
        post = blog.get(blog.post_id == get_post_id)
        return post.delete_instance()
    return False