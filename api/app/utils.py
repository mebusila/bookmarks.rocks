__author__ = 'Serban Carlogea'

from datetime import timedelta
from flask import make_response, request, current_app, abort
from functools import update_wrapper, wraps
import re
from models.user import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app import app


def crossdomain(origin=None, methods=None, headers=['Authorization'],
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def authorized(fn):
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.objects(id=data['id']).first()

    @wraps(fn)
    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
            return None
        user = verify_auth_token(request.headers['Authorization'])
        if user is None:
            abort(401)
            return None
        return fn(user=user, *args, **kwargs)
    return _wrap


def generate_auth_token(user=None, expiration=86400):
    if user:
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(user.id)})
    return None


def is_valid_email(email):
    if not email:
        return False
    return re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email)


def is_valid_password(password):
    if not password:
        return False
    return len(password) > 4


def is_valid_url(url):
    if not url:
        return None
    return len(url) > 4


def get_login_form_errors(email, password):
    errors = []

    if not is_valid_email(email):
        errors.append('Invalid email address')

    if not is_valid_password(password):
        errors.append('Invalid password')

    return errors


def get_bookmark(bookmark=None):
    return bookmark