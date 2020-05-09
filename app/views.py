import os
import datetime
from app.models import Posts, Users, Likes, Follows
from app.forms import LoginForm, PostsForm, RegistrationForm
from app import app, db, filefolder
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html')


@app.route('/api/users/register', methods=['POST'])
def register():
    """Accepts user information and saves it to the database"""
    return render_template('index.html')


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Accepts login credentials as username and password"""
    return render_template('index.html')


@app.route('/api/auth/logout', methods=['GET'])
def logout():
    """Logout a user"""
    return render_template('index.html')


@app.route('/api/users/<user_id>/posts', methods=['POST'])
def login():
    """Used for adding posts to the user's feed"""
    return render_template('index.html')


@app.route('/api/users/<user_id>/posts', methods=['GET'])
def login():
    """Returns a user's posts"""
    return render_template('index.html')


@app.route('/api/users/<user_id>/follow', methods=['POST'])
def login():
    """Create a follow relationship between the current user and the target user."""
    return render_template('index.html')


@app.route('/api/posts', methods=['GET'])
def login():
    """Returns all posts for all users"""
    return render_template('index.html')


@app.route('/api/posts/<post_id>/like', methods=['GET'])
def login():
    """Set a like on the current Post by the logged in User"""
    return render_template('index.html')

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