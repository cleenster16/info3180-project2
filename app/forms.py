from flask_wtf import FlaskForm
from wtforms import PasswordField, TextAreaField, StringField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Enter username")])
    password = PasswordField('Password', validators=[InputRequired()])

class PostsForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired("Please add a file"), FileAllowed(['png', 'jpg'], 'Images only!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Enter username")])
    password = PasswordField('Password', validators=[InputRequired(message="Enter password")])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(message="Email is required"), Email(message="Only Emails")])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!'), FileRequired()])
    register = SubmitField("Register")