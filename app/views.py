import os
from app import app, db, filefolder, token_key, iconFolder
from app.models import Posts, Users, Likes, Follows
from app.forms import LoginForm, RegistrationForm, PostsForm
import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename

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
             ids = jwt.decode(token, token_key)
             get_user_info = Users.query.filter_by(id=ids['user_id']).first()

        except jwt.ExpiredSignature:
            return jsonify({'code': 'expired_token', 'description': 'Your token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = ids['user_id']
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

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
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