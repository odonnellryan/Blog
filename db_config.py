from peewee import IntegerField, CharField, TextField, Model
import config


class NeoDB(Model):
    class Meta:
        database = config.DATABASE


class blog(NeoDB):
    post_id = IntegerField(primary_key=True)
    title = CharField()
    body = TextField()
    username = CharField()