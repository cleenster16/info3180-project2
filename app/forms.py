from flask_wtf import FlaskForm
from wtforms import PasswordField, TextAreaField, StringField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Enter username")])
    password = PasswordField('Password', validators=[InputRequired(message="Enter password")])

class PostsForm(FlaskForm):
    photo = FileField('Photo', FileRequired("Please add a file"), FileAllowed(['png', 'jpg'], 'Images only!'))
    caption = TextAreaField('Caption', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', validators=[InputRequired(message="Enter username")])
    _password = PasswordField('Password', validators=[InputRequired(message="Enter password")])
    first_name = TextAreaField('First Name', validators=[InputRequired()])
    last_name = TextAreaField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(message="Email is required"), Email(message="Only Emails")])
    location = TextAreaField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Photo', FileAllowed(['png', 'jpg'], 'Images only!'), FileRequired("Please add a file"))
