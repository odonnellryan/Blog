import db_config
blog = db_config.Posts
user_d = db_config.UserData


def check_if_post_exists(get_post_id):
    return blog.select().where(blog.post_id == get_post_id).exists()


def get_all_titles_and_ids():
    posts = {post.post_id : post.title for post in blog.select()}
    return posts


def get_latest_ten_posts():
    blog_posts = blog.select()
    posts = [post for post in blog_posts.order_by(blog.post_id.desc()).limit(10)]
    return posts

def get_total_post_count():
    posts = blog.select().count()
    return posts


def get_visible_post_count():
    posts = blog.select().where(blog.visible == 1).count()
    return posts


def paginate_visible_posts(page):
    paginate_count = 10
    posts = blog.select().where(blog.visible == 1).order_by(blog.post_id).paginate(page, paginate_count)
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
        post = blog
        update = post.update(title=get_title, body=get_body).where(post.post_id == get_post_id)
        update.execute()
        return True
    return False


def delete_post(get_post_id):
    if check_if_post_exists(get_post_id):
        post = blog.get(blog.post_id == get_post_id)
        return post.delete_instance()
    return False


#User Data related database queries

def update_all_data(get_title, get_subtitle, get_full_name, get_tags, get_footer_text):
    query = user_d.update(blog_title=get_title, blog_subtitle=get_subtitle, full_name=get_full_name,
                          tags=get_tags, footer_text=get_footer_text).where(user_d.id == 0)
    query.execute()


def update_title(get_title):
    title = user_d.update(blog_title=get_title).where(user_d.id == 0)
    title.execute()


def update_subtitle(get_subtitle):
    subtitle = user_d.update(blog_subtitle=get_subtitle).where(user_d.id == 0)
    subtitle.execute()


def update_name(get_full_name):
    name = user_d.update(full_name=get_full_name).where(user_d.id == 0)
    name.execute()


def update_tags(get_tag_list):
    tags = user_d.update(tags=get_tag_list).where(user_d.id == 0)
    tags.execute()


def update_footer_text(get_footer_text):
    footer_text = user_d.update(tags=get_footer_text).where(user_d.id == 0)
    footer_text.execute()


#Get user-configured data functions

def get_user_data():
    query = user_d.get(user_d.id == 0)
    return query


def get_tags():
    """returns tags in a comma-separated list"""
    query = user_d.get(user_d.id == 0)
    return query.tags


def get_username():
    query = user_d.get(user_d.id == 0)
    return query.username


def get_password(get_username):
    query = user_d.get(user_d.username == get_username)
    return query.password


def get_blog_title():
    query = user_d.get(user_d.id == 0)
    return query.blog_title


def get_blog_subtitle():
    query = user_d.get(user_d.id == 0)
    return query.blog_subtitle


def get_footer_text():
    query = user_d.get(user_d.id == 0)
    return query.footer_text