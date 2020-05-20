from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    biography = db.Column(db.String(1000), nullable=False)
    profile_photo = db.Column(db.String(200), nullable=False)
    joined_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    posts = db.relationship('Posts', backref='user', passive_deletes=True, lazy=True cascade="all")
    likes = db.relationship('Likes', backref='user', passive_deletes=True, lazy=True cascade="all")
    followers = db.relationship('Follows', backref='user', passive_deletes=True, lazy=True cascade="all")

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id) #Python2 support
        except NameError:
            return str(self.id) #Python3 support
    
    def __repr__(self):
        return '<User %r>' % (self.username)

class Posts(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'),nullable=False)
    photo = db.Column(db.String(80), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    likes = db.relationship('Likes', backref='post', passive_deletes=True, lazy=True)

    def __init__(self, user_id, photo, caption):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

class Likes(db.Model):
    __tablename__ = "Likes"
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='_user_post_'), )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('Posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

class Follows(db.Model):
    __tablename__ = "Follows"
    __table_args__ = (db.UniqueConstraint('user_id', 'follower_id', name='__user_follower__'), )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    follower_id = db.Column(db.Integer, nullable=False)
    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:    
            return str(self.id)  # python 3 support