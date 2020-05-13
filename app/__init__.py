from flask import Flask
from flask-login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] =""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TOKEN_SECRET'] = 'somethingsecret'
app.config['UPLOAD_FOLDER'] = './app/static/uploads'
app.config['ICONS_FOLDER'] = '.app/static/icons'

csrf = CSRFProtect(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
filefolder = app.config['UPLOAD_FOLDER']
token_key = app.config['TOKEN_SECRET']
iconFolder = app.config['ICONS_FOLDER']

from app import views