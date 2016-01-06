__author__ = 'Serban Carlogea'


from app.models.user import User
from flask import request, jsonify
from app.utils import crossdomain, generate_auth_token, get_login_form_errors, authorized
from . import resources

@resources.route('/users', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def register():
    """
    .. http:post:: /users

        Register a new user.

        **Example request**:

        .. sourcecode:: http

            POST /users HTTP/1.1
            Host: example.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
                "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND...",
                "user": {
                    "id": "558ec457a6758a12a05..."
                    ...
                }
            }

        .. sourcecode:: http

            HTTP/1.1 400 BAD REQUEST
            Content-Type: text/javascript

            {
                "errors": [
                    "Email already taken"
                ]
            }

        :form email: user email address
        :form password: user password

        :resheader Content-Type: application/json
        :statuscode 200: no error
        :statuscode 400: error
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    errors = get_login_form_errors(email, password)

    if errors:
        return jsonify(errors=errors), 400

    user = User.objects(email=email)
    if user:
        return jsonify(errors=['Email already taken']), 400

    user = User(email=email)
    user.hash_password(password)
    if user.save():
        token = generate_auth_token(user)
        return jsonify(user=user.to_dict(), token=token), 200

    return jsonify(errors=['Undefined error']), 400


@resources.route('/users/token', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def login():
    """
    .. http:post:: /users/token

        Returns authorization token

        **Example request**:

        .. sourcecode:: http

            POST /users/token HTTP/1.1
            Host: example.com
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
                "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND..."
            }

        .. sourcecode:: http

            HTTP/1.1 401 UNAUTHORIZED
            Content-Type: text/javascript

            {
                "errors": [
                    "Invalid login"
                ]
            }

        :form email: user email address
        :form password: user password

        :statuscode 200: no error
        :statuscode 401: Invalid user credentials
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    errors = get_login_form_errors(email, password)

    if errors:
        return jsonify(errors=errors), 401

    token = None
    user = User.objects(email=email).first()
    if user and user.verify_password(password):
        token = generate_auth_token(user)

    if token and user:
        return jsonify(token=token), 200

    return jsonify(errors=['Invalid login']), 401


@resources.route('/users/me', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def get(user=None):
    """
    .. todo::
        Implementation
    """
    pass


@resources.route('/users/me', methods=['PUT', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def edit(user=None):
    """
    .. todo::
        Implementation
    """
    pass