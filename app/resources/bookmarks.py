__author__ = 'Serban Carlogea'


from app.models.bookmark import Bookmark
from mongoengine import ValidationError
from flask import request, jsonify, abort
from app.utils import crossdomain, authorized, is_valid_url
import datetime
from . import resources


@resources.route('/bookmarks', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def bookmarks(user=None):
    """

    .. http:get:: /bookmarks

        Returns a list of bookmarks

        **Example request**:

        .. sourcecode:: http

            GET /bookmarks HTTP/1.1
            Host: example.com
            Authorization: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND...
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
                "bookmarks": [
                    {
                        "created_at": "2015-06-27 10:34:03.748000",
                        "description": "Representational State Transfer ( REST ) is a software architecture style consisting of guidelines and best practices for creating scalable web services.",
                        "id": "558e7c1b8b04d503968f6513",
                        "tags": [],
                        "title": "Representational state transfer - Wikipedia, the free encyclopedia",
                        "updated_at": "2015-06-27 10:34:03.748000",
                        "url": "https://en.wikipedia.org/wiki/Representational_state_transfer",
                        "user": "54f8c4458b04d5046753c6c2"
                    },
                    ...
                ]
            }

        :query offset: offset number. default is 0
        :query limit: limit number. default is 30
        :reqheader Authorization: User authorization token
        :statuscode 200: no error
        :statuscode 401: Invalid token

    """

    bookmarks = [bookmark.to_dict() for bookmark in Bookmark.objects(user=user, deleted_at=None).all()]
    return jsonify(bookmarks=bookmarks), 200


@resources.route('/bookmarks/<bookmark_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def bookmark(user=None, bookmark_id=None):
    """

    .. http:get:: /bookmarks/<bookmark_id>

        Get a bookmark by id

        **Example request**:

        .. sourcecode:: http

            GET /bookmarks/55282038a6758a110aa29695 HTTP/1.1
            Host: example.com
            Authorization: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND...
            Accept: application/json


        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
                "created_at": "2015-03-22 18:58:38.621000",
                "description": "In LESS I can apply two rules like this to affect text styling of links to hide underline unless hovered",
                "id": "550f02cea6758a98c5208f53",
                "screenshot": null,
                "tags": [],
                "title": "Can I apply a :hover psuedo selector with the LESS css markup?",
                "updated_at": "2015-03-22 18:58:40.632000",
                "url": "http://stackoverflow.com/questions/8491835/can-i-apply-a-hover-psuedo-selector-with-the-less-css-markup",
                "user": "54fb0af3b153ff033027f4c9"
            }

        :param bookmarks_id: bookmark's unique id
        :type bookmarks_id: str

        :reqheader Authorization: User authorization token
        :statuscode 200: No error
        :statuscode 404: Bookmark not found
        :statuscode 401: Invalid token

    """
    try:
        bookmark = Bookmark.objects(id=bookmark_id, user=user, deleted_at=None).first()
        if bookmark:
            return jsonify(bookmark.to_dict()), 200
        abort(404)
    except ValidationError:
        abort(404)


@resources.route('/bookmarks', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def add(user=None):
    """
    .. http:post:: /bookmarks

        Add new bookmark to user collection

        **Example request**:

        .. sourcecode:: http

            POST /bookmarks HTTP/1.1
            Host: example.com
            Authorization: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND...
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: text/javascript

            {
                "created_at": "2015-03-22 18:58:38.621000",
                "description": "In LESS I can apply two rules like this to affect text styling of links to hide underline unless hovered",
                "id": "550f02cea6758a98c5208f53",
                "screenshot": null,
                "tags": [],
                "title": "Can I apply a :hover psuedo selector with the LESS css markup?",
                "updated_at": "2015-03-22 18:58:40.632000",
                "url": "http://stackoverflow.com/questions/8491835/can-i-apply-a-hover-psuedo-selector-with-the-less-css-markup",
                "user": "54fb0af3b153ff033027f4c9"
            }

        :form url: Bookmark url
        :reqheader Authorization: User authorization token
        :statuscode 200: No error
        :statuscode 404: Bookmark not found
        :statuscode 401: Invalid token

    """
    url = request.form.get('url', None)
    if not is_valid_url(url):
        return jsonify(errors=['Dude, what\'s wrong with you ?', 'Invalid Bookmark Url']), 400

    bookmark = Bookmark.objects(url=url, user=user).first()
    if bookmark is None:
        bookmark = Bookmark(url=url, user=user)

    bookmark.deleted_at = None
    if bookmark.save():
        return jsonify(bookmark.to_dict()), 200

    return jsonify(errors=[bookmark.to_dict()]), 400


@resources.route('/bookmarks/<bookmark_id>', methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*')
@authorized
def delete(user=None, bookmark_id=None):
    """

    .. http:delete:: /bookmarks/<bookmark_id>

        Delete a bookmark by id

        **Example request**:

        .. sourcecode:: http

            DELETE /bookmarks/55282038a6758a110aa29695 HTTP/1.1
            Host: example.com
            Authorization: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNTQzOTk0OSwiaWF0IjoxND...
            Accept: application/json


        :param bookmarks_id: bookmark's unique id
        :type bookmarks_id: str
        :reqheader Authorization: User authorization token
        :statuscode 200: No error
        :statuscode 404: Bookmark not found
        :statuscode 401: Invalid token

    """
    bookmark = Bookmark.objects(id=bookmark_id, user=user, deleted_at=None).first()
    if bookmark:
        bookmark.deleted_at = datetime.datetime.now()
        if bookmark.save():
            return jsonify(), 200
        return jsonify(errors=[bookmark.to_dict()]), 400

    abort(404)