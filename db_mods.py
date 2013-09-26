from collections import OrderedDict
import db_config

blog = db_config.Posts
user_d = db_config.UserData

# Helper Function

def post_tag_identifier(get_tags) :
    """
    Gets a dictionary returned by WTForms of the boolean tag values, then returns the tags that are true (selected)
    as a string (to insert into db)
    """

    post_tags = []

    for tag in get_tags :
        if get_tags[tag].data :
            post_tags.append(tag)

    tags = ",".join(post_tags)

    return tags


def tag_parser(get_tags) :
    """
    Gets tags in a list and parses them, removing spaces before and after words
    """
    if get_tags :
        tags = get_tags.split(",")
        _tags = [x.strip(" ") for x in tags]
        return ",".join(_tags)
    else :
        return None


# get post information


def check_if_post_exists(get_post_id) :
    return blog.select().where(blog.id == get_post_id).exists()


def get_all_titles_and_ids() :
    posts = OrderedDict([post.id, post.title] for post in blog.select().order_by(blog.id.desc()))
    return posts


def get_latest_ten_posts() :
    blog_posts = blog.select()
    posts = [post for post in blog_posts.order_by(blog.id.desc()).limit(10)]
    return posts


def get_total_post_count() :
    posts = blog.select().count()
    return posts


def get_visible_post_count() :
    posts = blog.select().where(blog.visible == 1).count()
    return posts


def paginate_visible_posts(page) :
    paginate_count = 10
    posts_page = blog.select().where(blog.visible == 1).order_by(blog.id.desc()).paginate(page, paginate_count)
    for post in posts_page :
        if post.tags :
            post.tags = post.tags.split(",")
    return posts_page


def get_post_content(post_id) :
    post = {}
    for _ in blog.select().where(blog.id == post_id) :
        post['title'] = _.title
        post['body'] = _.body
        try :
            post['images'] = _.images.split(",")
        except AttributeError :
            post['images'] = None
        try :
            post['tags'] = _.tags.split(",")
        except AttributeError :
            post['tags'] = None
    return post


def check_user(get_title, get_user) :
    return blog.select().where(blog.title == get_title, blog.username == get_user).exists()


def add_new_post(get_title, get_body, get_tags, get_comma_image_list=None) :
    tags = post_tag_identifier(get_tags)
    if not tags :
        tags = None
    insert_blog = blog()
    insert_blog.title = get_title
    insert_blog.body = get_body
    insert_blog.tags = tags
    insert_blog.images = get_comma_image_list
    insert_blog.save()
    return insert_blog.id


def edit_post(get_title, get_body, get_post_id, get_tags, get_comma_image_list) :
    tags = post_tag_identifier(get_tags)
    if not tags :
        tags = None
    if check_if_post_exists(get_post_id) :
        post = blog
        update = post.update(title=get_title, body=get_body, tags=tags, images=get_comma_image_list
        ).where(post.id == get_post_id)
        update.execute()
        return get_post_id
    return False


def search_by_tag(get_tag) :
    posts = blog.select().where(blog.tags % ('%{0}%'.format(get_tag))).order_by(blog.id.desc())
    for post in posts :
        if post.tags :
            post.tags = post.tags.split(",")
    return posts


def delete_post(get_post_id) :
    if check_if_post_exists(get_post_id) :
        post = blog.get(blog.id == get_post_id)
        return post.delete_instance()
    return False


#User Data related database queries


def update_all_data(get_title=None, get_subtitle=None, get_full_name=None, get_tags=None, get_footer_text=None) :
    tags = tag_parser(get_tags)
    query = user_d.update(blog_title=get_title, blog_subtitle=get_subtitle, full_name=get_full_name,
                          tags=tags, footer_text=get_footer_text).where(user_d.id == 0)
    query.execute()


def update_title(get_title) :
    title = user_d.update(blog_title=get_title).where(user_d.id == 0)
    title.execute()


def update_subtitle(get_subtitle) :
    subtitle = user_d.update(blog_subtitle=get_subtitle).where(user_d.id == 0)
    subtitle.execute()


def update_name(get_full_name) :
    name = user_d.update(full_name=get_full_name).where(user_d.id == 0)
    name.execute()


def update_tags(get_tag_list) :
    _tags = tag_parser(get_tags)
    tags = user_d.update(tags=_tags).where(user_d.id == 0)
    tags.execute()


def update_footer_text(get_footer_text) :
    footer_text = user_d.update(tags=get_footer_text).where(user_d.id == 0)
    footer_text.execute()


#Get user-configured data functions


def get_user_data() :
    query = user_d.get(user_d.id == 0)
    return query


def get_tags() :
    """returns tags in a comma-separated list"""
    query = user_d.get(user_d.id == 0)
    return query.tags


def tag_array() :
    """returns tags in an array """
    try :
        return get_tags().split(',')
    except AttributeError :
        return None


def get_password(get_username) :
    query = user_d.get(user_d.username == get_username)
    return query.password


def get_blog_title() :
    query = user_d.get(user_d.id == 0)
    return query.blog_title


def get_blog_subtitle() :
    query = user_d.get(user_d.id == 0)
    return query.blog_subtitle


def get_footer_text() :
    query = user_d.get(user_d.id == 0)
    return query.footer_text