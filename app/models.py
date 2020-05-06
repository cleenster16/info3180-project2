from . import db

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(80))
    caption = db.Column(db.String(250))
    created_on = db.Column(db.DateTime)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(250))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    biography = db.Column(db.Text)
    profile_photo = db.Column(db.String(80))
    joined_on = db.Column(db.DateTime)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)

def is_authenticated(self):
    return True    

def is_active(self):
    return True    

def is_anonymous(self):
    return False    

def get_id(self):
    try:
        return unicode(self.id)  # python 2 support    
    except NameError:    
        return str(self.id)  # python 3 support         