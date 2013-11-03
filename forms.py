from wtforms import Form, TextField, TextAreaField, validators, BooleanField, FileField, PasswordField

class NewPost(Form):
    post_title = TextField(u'Post Title', [validators.Length(min=1)])
    post_body = TextAreaField(u'Post Body', [validators.Length(min=1)])
    published = BooleanField(u'Check to Publish When Saved')

class UploadImages(Form):
    post_image = FileField(u'Upload Image')

class Login(Form):
    username = TextField(u'Username', [validators.Length(min=1)])
    password = PasswordField(u'Password', [validators.Length(min=1)])

class SetLogin(Form):
    username = TextField(u'Username *', [validators.Length(min=1)])
    password = PasswordField(u'Password *', [validators.Length(min=1)])
    confirm_password = PasswordField(u'Confirm Password *', [validators.EqualTo('password',
                                                                              message='Your passwords must match.')])
class ChangeLogin(Form):
    username = TextField(u'Current Username', [validators.Length(min=1)])
    password = PasswordField(u'Current Password', [validators.Length(min=1)])
    new_username = TextField(u'New Username (if desired)')
    new_password_1 = PasswordField(u'New Password (if desired)', [validators.Length(min=1)])
    new_password_2 = PasswordField(u'New Password (again)', [validators.EqualTo('new_password_1',
                                                                                message='Your passwords must match.')])
class Commit(Form):
    commit = BooleanField(U'Commit to Flat File')

class Delete(Form):
    delete = BooleanField(U'Check to Delete Post')

class BlogSettings(Form):
    blog_title = TextField(u'Blog Title')
    blog_subtitle = TextField(u'Blog SubTitle')
    full_name = TextField(u'Display Name')
    footer_text = TextAreaField(u'Footer Text (HTML and Markdown allowed)')
    tags = TextField(u'Comma-Separated Interest Tags')
    logo_image = FileField(u'Upload Any Size JPG Logo. Overwrites Existing Logo')