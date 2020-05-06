from flask_wtf import FlaskForm
from wtforms import PasswordField, TextAreaField, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = TextAreaField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class PostsForm(FlaskForm):
    photo = FileField('Photo', FileRequired(), FileAllowed()])
    caption = TextAreaField('Caption', validators=[InputRequired()])

class Register(FlaskForm):
    user_name = TextAreaField('Username', validators=[InputRequired()])
    _password = PasswordField('Password', validators=[InputRequired()])
    first_name = TextAreaField('First Name', validators=[InputRequired()])
    last_name = TextAreaField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    location = TextAreaField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Photo', FileAllowed(['png', 'jpg']), FileRequired())
