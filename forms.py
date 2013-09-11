from wtforms import Form, TextField, TextAreaField, validators, BooleanField, FileField, PasswordField

class NewPost(Form):
    post_title = TextField(u'Post Title', [validators.Length(min=1)])
    post_body = TextAreaField(u'Post Body', [validators.Length(min=1)])


class UploadImages(Form):
    post_image = FileField(u'Upload Image')


class Login(Form):
    username = TextField(u'Username', [validators.Length(min=1)])
    password = PasswordField(u'Password', [validators.Length(min=1)])


class ForgotPassword(Form):
    username = TextField(u'Username', [validators.Length(min=1)])
    email = TextField(u'Email', [validators.Length(min=1)])


class ChangeLogin(Form):
    username = TextField(u'Current Username', [validators.Length(min=1)])
    password = PasswordField(u'Current Password', [validators.Length(min=1)])
    new_username = TextField(u'New Username (if desired)')
    new_password_1 = PasswordField(u'New Password (if desired)')
    new_password_2 = PasswordField(u'New Password (again)')


class Commit(Form):
    commit = BooleanField(U'Commit to Flat File')


class Delete(Form):
    delete = BooleanField(U'Check to Delete Post')


class BlogSettings(Form):
    blog_title = TextField(u'Blog Title')
    blog_subtitle = TextField(u'Blog SubTitle')
    full_name = TextField(u'Display Name')
    footer_text = TextAreaField(u'Footer Text (HTML and Markdown allowed)')
    tags = TextField(u'Comma-Separated Interest Tags (max-length 2000 characters)', [validators.Length(max=2000)])
    logo_image = FileField(u'Upload Any Size JPG Logo. Overwrites existing image')
