__author__ = 'Serban Carlogea'

from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = MongoEngine(app)

from app.resources import users
from app.resources import bookmarks
from app.resources import tags
