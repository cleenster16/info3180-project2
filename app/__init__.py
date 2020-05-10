from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

TOKEN_SECRET = 'somethingsecret'
UPLOAD_FOLDER = './app/static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] =""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
csrf = CSRFProtect(app)

db = SQLAlchemy(app)

app.config.from_object(__name__)
filefolder = app.config['UPLOAD_FOLDER']
token_key = app.config['TOKEN_SECRET']

from app import views