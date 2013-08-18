from wtforms import Form, TextField, TextAreaField, validators, BooleanField

class NewPost(Form):
    post_title = TextField(u'Post Title', [validators.Length(min=1)])
    post_body = TextAreaField(u'Post Body', [validators.Length(min=1)])


class Login(Form):
    username = TextField(u'Username', [validators.Length(min=1)])
    password = TextField(u'Password', [validators.Length(min=1)])


class Commit(Form):
    commit = BooleanField(U'Commit to Flat File')