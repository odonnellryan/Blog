from peewee import IntegerField, CharField, TextField, Model, BlobField
import config


class Blog(Model):
    class Meta:
        database = config.DATABASE


class Posts(Blog):
    post_id = IntegerField(primary_key=True)
    title = CharField()
    body = TextField()
    visible = IntegerField()
    tags = CharField()


class UserData(Blog):
    full_name = CharField()
    footer_text = CharField()
    blog_subtitle = CharField()
    tags = CharField()
    blog_title = CharField()
    password = BlobField()
    username = CharField()