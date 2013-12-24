from peewee import IntegerField, TextField, Model, BlobField, \
    MySQLDatabase, SqliteDatabase, PrimaryKeyField, PostgresqlDatabase, ImproperlyConfigured, DateField

import datetime
import config

def database():
    if config.DATABASE_TYPE.lower() == 'mysql':
        database = MySQLDatabase(config.DATABASE, user=config.DATABASE_USER, passwd=config.DATABASE_PASSWORD)
    elif config.DATABASE_TYPE.lower() == 'prostgres':
        database = PostgresqlDatabase(config.DATABASE, user=config.DATABASE_USER, passwd=config.DATABASE_PASSWORD)
    elif config.DATABASE_TYPE.lower() == 'sqlite':
        database = SqliteDatabase(config.DATABASE, user=config.DATABASE_USER, passwd=config.DATABASE_PASSWORD)
    else:
        raise ImproperlyConfigured
    return database

DB_OB = database()

class Blog(Model):
    class Meta:
        database = DB_OB

class Posts(Blog):
    id = PrimaryKeyField()
    title = TextField(null=True, default=None)
    url_title = TextField(null=True, default=None)
    body = TextField(null=True, default=None)
    visible = IntegerField(null=True, default=None)
    tags = TextField(null=True, default=None)
    created_date = DateField(default=datetime.date.today())
    images = TextField(null=True, default=None)

class UserData(Blog):
    id = PrimaryKeyField()
    full_name = TextField(null=True, default=None)
    footer_text = TextField(null=True, default=None)
    blog_subtitle = TextField(null=True, default=None)
    tags = TextField(null=True, default=None)
    blog_title = TextField(null=True, default=None)
    password = BlobField(null=True, default=None)
    username = TextField(null=True, default=None)
    forgot_password = BlobField(null=True, default=None)
    email = TextField(null=True, default=None)