from peewee import IntegerField, CharField, TextField, Model, BlobField
import config


class Blog(Model):
    class Meta:
        database = config.DATABASE


class Posts(Blog):
    title = CharField()
    url_title = CharField()
    body = TextField()
    visible = IntegerField()
    tags = CharField()
    images = CharField()


class UserData(Blog):
    full_name = CharField()
    footer_text = CharField()
    blog_subtitle = CharField()
    tags = CharField()
    blog_title = CharField()
    password = BlobField()
    username = CharField()
    forgot_password = BlobField()
    email = CharField()


def create_tables():
    Blog.create()
    Posts.create()
    UserData.create()