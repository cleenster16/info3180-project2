import os
from app import app, db, filefolder, iconFolder, login_manager
from app.models import Posts, Users, Likes, Follows
from app.forms import LoginForm, RegistrationForm, PostsForm
import datetime
from flask import g, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from functools import wraps
import base64

import jwt

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401
        sections = auth.split()
        if sections[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with bearer'}), 401 
        elif len(sections) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(sections) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must bearer + \s + token'}), 401
         
        token = sections[1]
        try:
            ids = jwt.decode(token, app.config['SECRET_KEY'])

        except jwt.ExpiredSignature:
            return jsonify({'code': 'expired_token', 'description': 'Your token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = ids
        return f(*args, **kwargs)
    return decorated

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/api/users/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database"""
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        photo = form.photo.data
        photoPath = assignFilename(photo)

        try:
            user = Users(username, password, firstname, lastname, email, location, biography, photoPath)
            if user is not None:
                db.session.add(user)
                db.session.commit()
                uploadFile(photo)
                info = [{"message": "User successfully registered"}]
                return jsonify(result=info), 201

        except Exception as e:
            print(e)
            db.session.rollback()
            error = "Server Error. Try again."
            return jsonify(error=error), 401

    all_errors = form_errors(form)
    return jsonify(errors=all_errors)

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password"""
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = db.session.query(Users).filter_by(username = username).first()
        if check_password_hash(user.password, password):
            login_user(user)

            ids = {'user' : user.username}
            jwt_token = jwt.encode(ids, app.config['SECRET_KEY'], algorithm = 'HS256').decode('utf-8')
        
            success = "User successfully logged in."
            return jsonify(message=success, token=jwt_token, user_id=user.id)

        error = "Incorrect username or password."
        return jsonify(error=error), 401

    all_errors = form_errors(form)
    return jsonify(errors=all_errors)

@app.route('/api/auth/logout', methods=['GET'])
def logout():
    logout_user()

    success = "User successfully logged out."
    return jsonify(message=success)

@app.route('/api/users/<user_id>', methods=['GET'])
@auth_required
def userProfile(user_id):
    try:
        user = db.session.query(Users).filter_by(id=user_id).first()
        #check if the current user(signed in) is following the user of the profile being viewed
        isFollowing = current_user.id in [ follower.follower_id for follower in user.followers]

        current = {"id": user.id, "username": user.username, "firstname": user.firstname, 
        "lastname": user.lastname, "email": user.email, "location": user.location, 
        "biography": user.biography, "profile_photo": os.path.join('./static/uploads', user.profile_photo), 
        "joined": user.joined_on.strftime("%b %Y"), "isFollowing": isFollowing, "posts": []}

        return jsonify(user=current)

    except Exception as e:
        print(e)
        error = "internal server error"
        return jsonify(error=error), 401

@app.route('/api/users/<user_id>/posts', methods=['POST','GET'])
@auth_required
def userPosts(user_id):
    form = PostsForm()
    if request.method == "POST" and form.validate_on_submit() == True:
        try:
            caption = form.caption.data
            photo = assignFilename(form.photo.data)
            post = Posts(user_id, photo, caption)
            db.session.add(post)
            db.session.commit()
            
            #Flash message to indicate a post was added successfully
            success = "Successfully created a new post"
            return jsonify(message=success), 201
        except Exception as e:
            print(e)
            
            error = "Internal server error"
            return jsonify(error=error), 401
        
    else:
        try:
            #Gets the current user to add/display posts to
            userPosts = db.session.query(Posts).filter_by(user_id=user_id).all()
            
            posts = []
            for post in userPosts:
                p = {"id": post.id, "user_id": post.user_id, "photo": os.join('./static/uploads', post.photo), "description": post.caption, "created_on": post.created_on.strftime("%d %b %Y")}
                posts.append(p)
            
            return jsonify(posts=posts)
        except Exception as e:
            print(e)
            
            error = "Internal server error"
            return jsonify(error=error), 401
            
    #Flash message to indicate an error occurred
    failure = "Failed to create/display posts"
    return jsonify(error=failure), 401

@app.route('/api/users/<user_id>/follow', methods=['POST', 'GET'])
@auth_required
def userFollows(user_id):
    if request.method == 'POST':
        try:
            id = current_user.id
            follow = Follows(id, user_id)
            db.session.add(follow)
            db.session.commit()
            
            #Flash message to indicate a successful following
            success = "You are now following that user"
            return jsonify(message=success), 201
        except Exception as e:
            print(e)
            
            #Flash message to indicate that an error occurred
            failure = "Internal error. Failed to follow user"
            return jsonify(error=failure), 401
    else:
        try:
            followers = db.session.query(Follows).filter_by(user_id=user_id).all()
            return jsonify(followers=len(followers)), 201
        except Exception as e:
            print(e)
            
            error = "Internal server error!"
            return jsonify(error=error), 401

@app.route('/api/posts', methods=['GET'])
@auth_required
def allPosts():
    try:
        posts = []
        userPosts = db.session.query(Posts).order_by(Posts.created_on.desc()).all()
    
        for post in userPosts:

            likes = [like.user_id for like in post.likes]
            isLiked = current_user.id in likes
            p = {"id": post.id, "user_id": post.user_id, "photo": os.path.join(app.config['GET_FILE'], post.photo), "caption": post.caption, "created_on": post.created_on.strftime("%d %b %Y"), "likes": len(post.likes), "isLiked": isLiked}
            posts.append(p)
        return jsonify(posts=posts), 201
    except Exception as e:
        print(e)
        
        error = "Internal server error"
        return jsonify(error=error), 401

@app.route("/api/posts/<post_id>/like", methods=["POST"])
@auth_required
def likePost(post_id):
    post = db.session.query(Posts).filter_by(id=post_id).first()
    if current_user.is_authenticated():
        id = current_user.id
        like = Likes(id, post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify(message="Post Liked!", likes=len(post.likes)), 201
    
    #Flash message to indicate that an error occurred
    failure = "Failed to like post"
    return jsonify(error=failure)

###
# Helper Functions
###

#Assign a filename to a file
def assignFilename(_file):
    filename = secure_filename(_file.filename)
    return filename

#Save a file to the uploads folder
def uploadFile(upload):
    filename = secure_filename(upload.filename)
    upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.query(Users).get(int(id))

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")