import os
import datetime
import jwt
from functools import wraps
from app.models import Posts, Users, Likes, Follows
from app.forms import LoginForm, PostsForm, RegistrationForm
from app import app, db, filefolder, token_key
from flask import session, g, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html')


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
             ids = jwt.decode(token, token_key)
             get_user_info = Users.query.filter_by(id=ids['user_id']).first()

        except jwt.ExpiredSignature:
            return jsonify({'code': 'expired_token', 'description': 'Your token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = ids['user_id']
        return f(*args, **kwargs)
    return decorated


@app.route('/api/users/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database"""
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        location = request.form['location']
        biography = request.form['biography']
        photo = request.file['profile_photo']
        date_now = datetime.datetime.now()
        photo_file = secure_filename(photo.photo_file)
        user = Users(firstname = firstname, lastname = lastname, email = email, location = location, biography = biography, profile_photo = photo, joined_on = date_now, username = username, password = password)
        db.session.add(user)
        db.session.commit()
        photo.save(os.path.join(filefolder, photo_file))
        info = [{"message": "User successfully registered"}]
        return jsonify(result=info)
    all_errors = form_errors(form)
    error = [{'error': all_errors}]
    return jsonify(errors=error)


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password"""
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form['user_name']
        password = request.form['password']

        user = Users.query.filter_by(username = username, password = password).first()
        if user is None:
            return jsonify(errorM="Incorrect username or password")

        ids = {'user_id': user.id}
        token = jwt.encode(ids, token_key)
        session['userid'] = user.id;        
        return jsonify(info={'token': token, 'userid': user.id}, message = "User logged in!")
    all_errors = form_errors(form)
    error = [{'error': all_errors}]
    return jsonify(errors=error)


@app.route('/api/auth/logout', methods=['GET'])
@requires_auth
def logout():
    """Logout a user"""
    g.current_user = None
    session.pop('userid', None)
    return jsonify(message = "You have been logged out!")


@app.route('/api/users/<user_id>/posts', methods=['POST'])
def new_user_post():
    """Used for adding posts to the user's feed"""
    form = PostsForm()
    if request.method == "POST" and form.validate_on_submit():
        userid = user_id
        caption = request.form['caption']
        photo_posted = request.file['photo']
        date_now = datetime.datetime.now()
        photo_file = secure_filename(photo_posted.photo_file)
        post = Posts(userid = user_id, caption = caption, created_on = date_now, photo_posted = photo)
        db.session.add(post)
        db.session.commit()
        photo_posted.save(os.path.join(filefolder, photo_file))
        info = [{"message": "Post successfully created"}]
        return jsonify(result=info)


@app.route('/post/', methods=["GET", "POST"])
def post():
    post = g.current_user
    return render_template('post.html', post=post)


@app.route('/api/users/<user_id>/posts', methods=['GET'])
def get_post():
    """Returns a user's posts"""
    if request.method == "GET":
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'no user found'})
        user_posts = Posts.query.filter_by(id=userid).all()
        info = []
        for user_post in user_posts:
            post_info = {'id': user_post.id, 'user_id': user_post.user_id, 'photo': user_post.photo, 'caption': user_post.caption, 'created_on': user_post.created_on}
            info.append(post_info)
        return jsonify(data=info)
    all_errors = form_errors(form)
    error = [{'error': all_errors}]
    return jsonify(errors=error)


@app.route('/api/users/<user_id>/', methods=["GET"])
@requires_auth
def get_user(user_id):
    # Database for all post
    user = Users.query.filter_by(id=user_id).first()
    info = []

    # House dictionary
    if (int(user_id) == session['userid']):
        join = user.joined_on.strftime("%B %Y");
        user_info= {"userid": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "email": user.email, "location": user.location, "biography": user.biography,"photo": user.profile_photo, "joined_on": join}
        info.append(user_info)
        return jsonify(profile = info, is_user = True)
    join = user.joined_on.strftime("%B %Y");
    user_info= {"userid": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "email": user.email, "location": user.location, "biography": user.biography,"photo": user.profile_photo, "joined_on": join}
    output.append(user_info)
    return jsonify(profile = info)


@app.route('/api/posts/', methods=["GET"])
@requires_auth
def all_posts():
    # Database for all post
    posts = Posts.query.order_by(Posts.created_on.desc()).all()

    # House dictionary
    info = []
    for post in posts:
        user = Users.query.filter_by(id = post.user_id).first()
        like = Likes.query.filter_by(post_id = post.id).all()
        number_of_likes = []
        for likes in number_of_likes:
            number = {'test': 'counted'}
            number_of_likes.append(number)
        liked = Likes.query.filter_by(user_id = session['userid'], post_id = post.id).first()
        if (liked is None):
            like_check = False
        else:
            like_check = True
        date_posted = post.created_on.strftime("%d %b %Y");
        posted = {"postid": post.id, "userid": post.user_id, "username": user.username, "profile_photo": user.profile_photo, "photo": post.photo, "caption": post.caption, "created_on": post.created_on, "likes": number_of_likes, "like_check": like_check}
        info.append(posted)
    return jsonify(data = info)



@app.route('/api/users/<user_id>/followID', methods=["GET"])
@requires_auth
def follow_number(user_id):
    """Shows the amount of followers for a user"""
    follows = Follows.query.filter_by(user_id=user_id).all()
    number_of_followers = []
    for follow in follows:
        number = {'test': 'counted'}
        number_of_followers.append(number)
    return jsonify(follower=number_of_followers)


@app.route('/api/users/<user_id>/following', methods=['POST'])
@requires_auth
def follower_check(user_id):
    """Create a follow relationship between the current user and the target user."""
    check = Follows.query.filter_by(user_id = user_id, followID = session['userid']).first()
    if (check is None):
        return jsonify(following = False)
    return jsonify(following = True)


@app.route('/api/users/<user_id>/follow', methods=['POST'])
@requires_auth
def follow_user(user_id):
    """Saves the user you are following"""
    follow = Follows(user_id = user_id, followID = session['userid'])
    db.session.add(follow)
    db.session.commit()
    return jsonify(message= 'You are now following this user')


@app.route('/api/posts/<post_id>/like', methods=['GET'])
@requires_auth
def like(post_id):
    """Set a like on the current Post by the logged in User"""
    check_likes = Likes.query.filter_by(user_id=session['userid'], post_id=postid).first()
    if(check_likes is None):
        like = Likes(user_id = session['userid'], post_id = post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify(message='You have liked a post')
    return jsonify(DB = 'You already liked the post')


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