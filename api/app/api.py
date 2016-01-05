__author__ = 'Serban Carlogea'

from app import app
from flask import request, jsonify
from utils import crossdomain, is_email_address_valid, is_password_valid, authorized, is_url_valid
from models import User, Bookmark

@app.route('/users/token', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def login():
    if 'email' not in request.form:
        return jsonify(errors=['Email is required']), 401

    if 'password' not in request.form:
        return jsonify(errors=['Password is required']), 401

    token = User.generate_auth_token(request.form['email'], request.form['password'])
    if token:
        return jsonify(token=token), 200
    return jsonify(errors=['Invalid login']), 401


@app.route('/users', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def register():
    if 'email' not in request.form:
        return jsonify(errors=['Email is required']), 401

    if 'password' not in request.form:
        return jsonify(errors=['Password is required']), 401

    token = User.generate_auth_token(request.form['email'], request.form['password'])
    if token:
        return jsonify(token=token), 200

    user = User.objects(email=request.form['email'])
    if user:
        return jsonify(errors=['Email already taken']), 401

    if not is_email_address_valid(request.form['email']):
        return jsonify(errors=['Invalid email address']), 401

    if not is_password_valid(request.form['password']):
        return jsonify(errors=['Password too short']), 401

    user = User(email=request.form['email'])
    user.hash_password(request.form['password'])
    if user.save():
        token = User.generate_auth_token(request.form['email'], request.form['password'])
        return jsonify(token=token), 200

    return jsonify(errors=['Undefined error']), 401


@app.route('/bookmarks', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def add(user=None):
    if 'url' not in request.form:
        return jsonify(errors=['Dude, what\'s wrong with you ?', 'You are missing Bookmark Url']), 400
    if not is_url_valid(request.form['url']):
        return jsonify(errors=['Dude, what\'s wrong with you ?', 'Invalid Bookmark Url']), 400
    bookmark = Bookmark(url=request.form['url'], user=user)
    if bookmark.save():
        return jsonify(bookmark=bookmark.to_dict()), 200
    return jsonify(errors=[bookmark.to_dict()]), 400


@app.route('/bookmarks', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def bookmarks(user=None):
    _bookmarks = Bookmark.objects(user=user).all()
    return jsonify(bookmarks=[bookmark.to_dict() for bookmark in _bookmarks]), 200


@app.route('/bookmarks/<bookmark_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def bookmark(user=None):
    bookmark = Bookmark.objects(id=bookmark_id, user=user).first()
    if bookmark:
        if bookmark.updated_at is None:
            bookmark.fetch()
        return jsonify(bookmark=bookmark.to_dict()), 200
    return jsonify(errors=['Not Found']), 404


@app.route('/bookmarks/<bookmark_id>/update', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def update(user=None, bookmark_id=None):
    bookmark = Bookmark.objects(id=bookmark_id, user=user).first()
    if bookmark and bookmark.fetch():
        if bookmark.save():
            return jsonify(bookmark=bookmark.to_dict())
        return jsonify(bookmark=bookmark.to_dict()), 304
    return jsonify(errors=['Not Found']), 404